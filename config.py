import os

class Config:
    HEFENG_API_KEY = os.getenv("HEFENG_API_KEY", "YOUR_API_KEY_HERE")
    HEFENG_KEY_ID = os.getenv("HEFENG_KEY_ID", "TJGUJN8E5W")
    HEFENG_PRIVATE_KEY_PATH = os.getenv("HEFENG_PRIVATE_KEY_PATH", "密钥/ed25519-private.pem")

    WECOM_CORP_ID = os.getenv("WECOM_CORP_ID", "wwf3c53a68a102c7ca")
    WECOM_AGENT_ID = os.getenv("WECOM_AGENT_ID", "1000002")
    WECOM_APP_SECRET = os.getenv("WECOM_APP_SECRET", "KVj_6AnLUd640d3TtZ0tyFoRmuySEKDpLI94tcHuWoA")
    WECOM_TO_USER = os.getenv("WECOM_TO_USER", "YOUR_USER_ID_HERE")

    CITY = "上海"
    SCHEDULE_HOUR = 6
    SCHEDULE_MINUTE = 0

config = Config()
