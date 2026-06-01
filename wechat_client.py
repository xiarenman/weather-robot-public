import requests
from config import config

class WeChatClient:
    def __init__(self):
        self.corp_id = config.WECOM_CORP_ID
        self.agent_id = config.WECOM_AGENT_ID
        self.app_secret = config.WECOM_APP_SECRET
        self.webhook_url = config.WECOM_WEBHOOK_URL
        self.access_token = None

    def send_webhook_message(self, message, webhook_url=None):
        url = webhook_url or self.webhook_url
        if not url:
            raise Exception("Webhook URL is not configured")
        
        payload = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if data.get("errcode") != 0:
            raise Exception(f"Failed to send webhook message: {data}")
        return data

    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corp_id,
            "corpsecret": self.app_secret,
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("errcode") != 0:
            raise Exception(f"Failed to get access token: {data}")

        self.access_token = data.get("access_token")
        return self.access_token

    def send_message(self, message, to_user=None):
        if not self.access_token:
            self.get_access_token()

        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
        params = {"access_token": self.access_token}

        payload = {
            "touser": to_user or config.WECOM_TO_USER,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {"content": message},
        }

        response = requests.post(url, params=params, json=payload, timeout=10)
        data = response.json()

        if data.get("errcode") != 0:
            if data.get("errcode") in [40014, 42001]:
                self.get_access_token()
                return self.send_message(message, to_user)
            raise Exception(f"Failed to send message: {data}")

        return data

wechat_client = WeChatClient()
