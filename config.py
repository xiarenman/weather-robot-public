import os

class Config:
    HEFENG_API_KEY = os.getenv("HEFENG_API_KEY", "2a27458fdb1f4cebae9ad91dddb63fce")
    HEFENG_API_HOST = os.getenv("HEFENG_API_HOST", "n94nmv63jv.re.qweatherapi.com")

    WECOM_CORP_ID = os.getenv("WECOM_CORP_ID", "wwf3c53a68a102c7ca")
    WECOM_AGENT_ID = os.getenv("WECOM_AGENT_ID", "1000002")
    WECOM_APP_SECRET = os.getenv("WECOM_APP_SECRET", "KVj_6AnLUd640d3TtZ0tyFoRmuySEKDpLI94tcHuWoA")
    WECOM_TO_USER = os.getenv("WECOM_TO_USER", "JiangChongHao")

    CITY = "上海"
    SCHEDULE_HOUR = 6
    SCHEDULE_MINUTE = 0

config = Config()
