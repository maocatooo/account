import os
from dotenv import load_dotenv

# 加载 .env 文件
if not os.getenv("AppID"):
    print("load dotenv")
    load_dotenv()

settings = type("settings", (object,), {
    "API_V1_STR": "",
    "BACKEND_CORS_ORIGINS": ["*"],
    "PROJECT_NAME": "acc",
    "SECRET_KEY": "12333",
    "MySQLDSN": os.getenv("MySQLDSN"),
    "WeChatAppId": os.getenv("WeChatAppId"),
    "WeChatAppSecret": os.getenv("WeChatAppSecret"),
    "QcloudAsrAppId": os.getenv("QcloudAsrAppId"),
    "QcloudAsrSecretId": os.getenv("QcloudAsrSecretId"),
    "QcloudAsrSecretKey": os.getenv("QcloudAsrSecretKey"),
    "BaiduApiKey": os.getenv("BaiduApiKey"),
    "BaiduSecretKey": os.getenv("BaiduSecretKey"),
})
