from app.model import BookJournal, ID, AsrJournal
from app.core.config import settings
import requests
from typing import Union
from app.api.deps import CurrentUser
from app.curd import SessionDep
from sqlmodel import func, select
from app.model import Tag
from app.curd import create_book_journals
from datetime import datetime


def asr_to_journal(db: SessionDep, current_user: CurrentUser, a: AsrJournal) -> Union[BookJournal, None]:
    if len(a.describe) <= 5:
        return None
    ts = db.exec(select(Tag).where(Tag.uid == current_user.id)).all()
    tag_dict = {t.name: t.id for t in ts}
    res = work_shop(gen_prompt(f'今天是{datetime.now().strftime("%Y-%m-%d")},' + a.describe, tag_dict.keys()))
    print(res)
    bj = format_result(res, tag_dict)
    bj.book_id = a.book_id
    return create_book_journals(db, current_user.id, bj)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": settings.BaiduApiKey,
              "client_secret": settings.BaiduSecretKey}
    return str(requests.post(url, params=params).json().get("access_token"))


def format_result(input_str: str, tag_dict) -> BookJournal:
    bj = BookJournal()
    pairs = input_str.split(',')
    # 创建字典
    result = {}
    for pair in pairs:
        key, value = pair.split(':', 1)  # 以第一个冒号作为分割点
        result[key] = value
    bj.name = result.get("name")
    bj.date = result.get("datetime")
    bj.amount = result.get("amount")
    bj.tname = result.get("tag")
    bj.tid = tag_dict.get(bj.tname)
    return bj


template = """
您将从用户那得到一段文字, 解析相关内容并且返回相关的内容
示例的tag:
%s
输入:
%s
输出:
"""


def gen_prompt(input, tags):
    return template % (",".join(tags), input)


def gen_dialog(user_input, assistant_output):
    return (
        {
            "role": "user",
            "content": user_input,
        },
        {
            "role": "assistant",
            "content": assistant_output,
        },
    )


#
#
prompts = []
#
prompts.extend(
    gen_dialog(
        gen_prompt("今天是2023-08-01,今天出门买衣服花了100元", ["早饭,午饭,购物"]),
        """datetime:2023-08-01 12:00,amount:100,tag:购物,name:买衣服"""
    )
)
prompts.extend(
    gen_dialog(
        gen_prompt("今天是2023-08-02,昨天中午给肚肚买猫粮花了10块1毛", ["早饭,午饭,购物,宠物"]),
        """datetime:2023-08-01 12:00,amount:10.1,tag:宠物,name:买猫粮"""),
)
prompts.extend(
    gen_dialog(
        gen_prompt("今天是2023-08-03,前天早上吃米饭用了十一块钱", ["早饭,午饭,购物"]),
        """datetime:2023-08-01 08:00,amount:11,tag:早饭,name:吃米饭"""
    )
)
prompts.extend(
    gen_dialog(gen_prompt("今天是2024-05-20,今天买花花费88块八毛八", ["早饭,午饭,购物,礼物"]),
               """datetime:2023-08-01 12:00,amount:88.88,tag:礼物,name:买花"""
               )
)


def work_shop(content):
    print(content)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    msgs = []
    msgs.extend(prompts)
    msgs.append(
        {
            "role": "user",
            "content": content,
        },
    )
    data = {
        "messages": msgs
    }
    resp = requests.post(url, json=data)
    return resp.json().get("result")


if __name__ == "__main__":
    a = work_shop("""
您将从用户那得到一段文字, 解析相关内容并且返回相关的内容
示例的tag:
早饭,午饭,购物,饮料
输入:
今天是2024-05-05,今天买水花了3块
输出:
""")
    print(a)
