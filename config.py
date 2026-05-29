import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    HEFENG_API_KEY = os.getenv("HEFENG_API_KEY")
    HEFENG_API_HOST = os.getenv("HEFENG_API_HOST")

    WECOM_CORP_ID = os.getenv("WECOM_CORP_ID")
    WECOM_AGENT_ID = os.getenv("WECOM_AGENT_ID")
    WECOM_APP_SECRET = os.getenv("WECOM_APP_SECRET")
    WECOM_TO_USER = os.getenv("WECOM_TO_USER")
    WECOM_TOKEN = os.getenv("WECOM_TOKEN")
    WECOM_ENCODING_AES_KEY = os.getenv("WECOM_ENCODING_AES_KEY")

    CITY = os.getenv("CITY", "上海")
    SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", 6))
    SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", 0))

config = Config()
