import random
import time
import uuid
from datetime import timedelta
from datetime import datetime
from jose import JWTError, jwt
from app.core.config import settings
import requests
import hmac
import hashlib
import base64
ALGORITHM = "HS256"


def create_access_token(user_id: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "user_id": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_openid(code):
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.WeChatAppId}&secret={settings.WeChatAppSecret}&js_code={code}&grant_type=authorization_code"
    print(url)
    res = requests.get(url)
    openid = res.json().get("openid")
    return openid


def qcloud_asr_generate_url():
    kvs = {
        # // secretid	是	String	腾讯云注册账号的密钥 SecretId，可通过 API 密钥管理页面 获取
        "secretid": settings.QcloudAsrSecretId,
        # // timestamp	是	Integer	当前 UNIX 时间戳，单位为秒。如果与当前时间相差过大，会引起签名过期错误

        "timestamp": int(time.time()),
        # // expired	是	Integer	签名的有效期截止时间 UNIX 时间戳，单位为秒。expired 必须大于 timestamp 且 expired - timestamp 小于90天

        "expired": int(time.time()) + 86400,

        # // nonce	是	Integer	随机正整数。用户需自行生成，最长10位

        "nonce": random.randint(1, 999999999),
        # // engine_model_type

        "engine_model_type": "16k_zh",
        # // voice_id	是	String	音频流识别全局唯一标识，一个 websocket 连接对应一个，用户自己生成（推荐使用 uuid），最长128位。
        "voice_id": str(uuid.uuid4()),
        # // voice_format
        "voice_format": 1,
    }

    keys = sorted(kvs.keys())
    s = []
    for k in keys:
        s.append(f"{k}={kvs[k]}")

    url = "%s/asr/v2/%s?%s" % ("asr.cloud.tencent.com", settings.QcloudAsrAppId, "&".join(s))
    signature = generate_signature(settings.QcloudAsrSecretKey, url)
    import urllib.parse
    url = "%s://%s&signature=%s"%("wss", url, urllib.parse.quote(signature))
    return url


def generate_signature(secret_key, server_url):
    # 创建新的HMAC对象，使用SHA1哈希函数
    hmac_obj = hmac.new(secret_key.encode(), server_url.encode(), hashlib.sha1)

    # 计算HMAC值
    encrypted_str = hmac_obj.digest()

    # 将HMAC值编码为base64
    signature = base64.b64encode(encrypted_str).decode()
    return signature
