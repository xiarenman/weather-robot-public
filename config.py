import os

class Config:
    HEFENG_API_KEY = os.getenv("HEFENG_API_KEY", "YOUR_API_KEY_HERE")

    WECOM_CORP_ID = os.getenv("WECOM_CORP_ID", "YOUR_CORP_ID_HERE")
    WECOM_AGENT_ID = os.getenv("WECOM_AGENT_ID", "YOUR_AGENT_ID_HERE")
    WECOM_APP_SECRET = os.getenv("WECOM_APP_SECRET", "YOUR_APP_SECRET_HERE")
    WECOM_TO_USER = os.getenv("WECOM_TO_USER", "YOUR_USER_ID_HERE")

    CITY = "上海"
    SCHEDULE_HOUR = 6
    SCHEDULE_MINUTE = 0

config = Config()
