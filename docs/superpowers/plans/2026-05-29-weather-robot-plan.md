# 天气机器人实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个每日天气播报机器人，通过企业微信每天早上6点向用户发送个性化天气消息

**Architecture:** 基于Python的定时任务系统，通过和风天气API获取天气数据，生成个性化消息后通过企业微信应用推送

**Tech Stack:** Python 3.8+, requests, APScheduler, 和风天气API, 企业微信应用消息API

---

## 文件结构

```
weather-robot/
├── config.py              # 配置文件
├── weather_service.py     # 天气服务
├── message_generator.py   # 消息生成器
├── wechat_client.py       # 企业微信推送
├── scheduler.py           # 定时调度器
├── main.py                # 主入口
├── requirements.txt       # 依赖包
└── docs/
    └── superpowers/
        ├── plans/
        │   └── 2026-05-29-weather-robot-plan.md
        └── specs/
            └── 2026-05-29-weather-robot-design.md
```

---

## 任务列表

### 任务 1: 创建 requirements.txt

**Files:**
- Create: `e:\agent project\weather-robot\requirements.txt`

- [ ] **Step 1: 创建 requirements.txt**
```
requests>=2.28.0
APScheduler>=3.10.0
```

---

### 任务 2: 创建 config.py

**Files:**
- Create: `e:\agent project\weather-robot\config.py`

- [ ] **Step 1: 创建配置文件**
```python
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
```

---

### 任务 3: 创建 weather_service.py

**Files:**
- Create: `e:\agent project\weather-robot\weather_service.py`

- [ ] **Step 1: 创建天气服务**
```python
import requests
from config import config

class WeatherService:
    def __init__(self):
        self.api_key = config.HEFENG_API_KEY
        self.city = config.CITY

    def get_weather(self):
        url = f"https://devapi.qweather.com/v7/weather/now"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}")

        return self._parse_weather_data(data)

    def get_daily_forecast(self):
        url = f"https://devapi.qweather.com/v7/weather/3d"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}")

        return self._parse_forecast_data(data)

    def _get_location_code(self):
        city_codes = {
            "上海": "101020100",
        }
        return city_codes.get(self.city, "101020100")

    def _parse_weather_data(self, data):
        now = data.get("now", {})
        return {
            "temp": now.get("temp"),
            "feels_like": now.get("feelsLike"),
            "humidity": now.get("humidity"),
            "wind_dir": now.get("windDir"),
            "wind_scale": now.get("windScale"),
            "weather_text": now.get("text"),
            "precip": now.get("precip"),
        }

    def _parse_forecast_data(self, data):
        daily = data.get("daily", [])[0] if data.get("daily") else {}
        return {
            "temp_max": daily.get("tempMax"),
            "temp_min": daily.get("tempMin"),
            "precip_prob": daily.get("pop"),
        }

weather_service = WeatherService()
```

---

### 任务 4: 创建 message_generator.py

**Files:**
- Create: `e:\agent project\weather-robot\message_generator.py`

- [ ] **Step 1: 创建消息生成器**
```python
import random
from datetime import datetime

GREETINGS = [
    "早上好，今天是元气满满的一天！来看看天气吧～",
    "早啊！睡得好吗？来瞅瞅今天的天气～",
    "新的一天，新的天气！让我来给你播报一下～",
    "起床啦！让我看看外面是什么天气～",
    "早起的鸟儿有虫吃，早起的你有天气看！",
    "嘿，醒醒！天气播报员准时上线～",
    "早上好呀！天气预报已新鲜出炉，请查收～",
    "新的一天开始了～让我来告诉你今天适不适合出门浪！",
]

WEATHER_COMPLAINTS = [
    "这天气热得我都想原地蒸发了，但至少比上周的梅雨季强吧？且行且珍惜！",
    "太阳公公今天是吃了火药吗？出门五分钟，流汗两小时！",
    "这温度，我躺在床上是铁板烧，出门是蒸笼，老天爷你是认真的吗？",
    "感觉今天出门就会被融化，但想想工资，还是得去上班啊！",
    "这鬼天气，我怀疑老天爷在练魔法，温度都能飙到这种程度！",
    "早上起来看到这温度，我默默打开了空调，然后陷入沉思——电费好贵。",
    "今天的阳光很热情，像极了催我上班的领导，我们还是做朋友吧。",
    "这天气出门需要勇气，毕竟我和烤肉之间只差一把孜然了。",
]

class MessageGenerator:
    def generate(self, weather_data, forecast_data):
        greeting = random.choice(GREETINGS)
        complaint = random.choice(WEATHER_COMPLAINTS)

        temp = weather_data["temp"]
        feels_like = weather_data["feels_like"]
        humidity = weather_data["humidity"]
        wind_dir = weather_data["wind_dir"]
        wind_scale = weather_data["wind_scale"]
        weather_text = weather_data["weather_text"]

        temp_max = forecast_data["temp_max"]
        temp_min = forecast_data["temp_min"]
        precip_prob = forecast_data["precip_prob"]

        today = datetime.now()
        date_str = today.strftime("%Y年%m月%d日")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()]

        clothing = self._get_clothing_advice(temp, weather_text)
        umbrella = self._get_umbrella_advice(precip_prob)

        message = f"""☀️ {config.CITY}今日天气（{date_str} {weekday}）

{greeting}

🌡️ 气温：{temp}°C（今日高温{temp_max}°C，低温{temp_min}°C，体感温度{feels_like}°C）
💧 湿度：{humidity}%
🌬️ 风力：{wind_dir}{wind_scale}级
🌤️ 天气状况：{weather_text}

👔 穿着建议：{clothing}

{umbrella}

💬 {complaint}"""

        return message

    def _get_clothing_advice(self, temp, weather_text):
        if temp >= 35:
            return "今天热到爆炸！建议穿轻薄透气的短袖短裤，别忘了随时补充水分哦～"
        elif temp >= 30:
            return "今天阳光明媚，适合穿轻薄短袖或长裙，出门记得防晒哦～"
        elif temp >= 25:
            return "温度刚刚好！穿件短袖或者薄外套就很舒服啦～"
        elif temp >= 20:
            return "早晚有点凉，建议穿件薄外套或长袖，别感冒了哦～"
        elif temp >= 15:
            return "今天有点凉飕飕的，记得加件外套或穿件薄毛衣～"
        elif temp >= 10:
            return "冷空气来了！建议穿厚外套或毛衣，别冻着自己～"
        else:
            return "今天真的很冷！羽绒服棉袄什么的都穿上吧，保暖要紧！"

    def _get_umbrella_advice(self, precip_prob):
        if precip_prob >= 80:
            return f"🌧️ 降雨概率：{precip_prob}%，今天大概率会下雨！出门一定要带伞，别被淋成落汤鸡！"
        elif precip_prob >= 50:
            return f"🌧️ 降雨概率：{precip_prob}%，有可能下雨，包里备把伞比较保险～"
        elif precip_prob >= 20:
            return f"🌧️ 降雨概率：{precip_prob}%，大概率不会下雨，但包里可以备把伞以防万一～"
        else:
            return f"🌧️ 降雨概率：{precip_prob}%，放心出门，应该不会下雨，不用带伞啦～"

message_generator = MessageGenerator()
```

---

### 任务 5: 创建 wechat_client.py

**Files:**
- Create: `e:\agent project\weather-robot\wechat_client.py`

- [ ] **Step 1: 创建企业微信客户端**
```python
import requests
from config import config

class WeChatClient:
    def __init__(self):
        self.corp_id = config.WECOM_CORP_ID
        self.agent_id = config.WECOM_AGENT_ID
        self.app_secret = config.WECOM_APP_SECRET
        self.access_token = None

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
            if data.get("errcode") == 40014:
                self.get_access_token()
                return self.send_message(message, to_user)
            raise Exception(f"Failed to send message: {data}")

        return data

wechat_client = WeChatClient()
```

---

### 任务 6: 创建 scheduler.py

**Files:**
- Create: `e:\agent project\weather-robot\scheduler.py`

- [ ] **Step 1: 创建定时调度器**
```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from config import config
from weather_service import weather_service
from message_generator import message_generator
from wechat_client import wechat_client

def send_daily_weather():
    try:
        weather_data = weather_service.get_weather()
        forecast_data = weather_service.get_daily_forecast()
        message = message_generator.generate(weather_data, forecast_data)
        wechat_client.send_message(message)
        print(f"Weather message sent successfully at {datetime.now()}")
    except Exception as e:
        print(f"Failed to send weather message: {e}")

def start_scheduler():
    scheduler = BlockingScheduler()
    trigger = CronTrigger(
        hour=config.SCHEDULE_HOUR,
        minute=config.SCHEDULE_MINUTE,
    )
    scheduler.add_job(send_daily_weather, trigger)
    print(f"Scheduler started. Weather message will be sent daily at {config.SCHEDULE_HOUR}:{config.SCHEDULE_MINUTE:02d}")
    scheduler.start()

if __name__ == "__main__":
    from datetime import datetime
    send_daily_weather()
```

---

### 任务 7: 创建 main.py

**Files:**
- Create: `e:\agent project\weather-robot\main.py`

- [ ] **Step 1: 创建主入口**
```python
from scheduler import start_scheduler

if __name__ == "__main__":
    print("Weather Robot starting...")
    start_scheduler()
```

---

### 任务 8: 初始化 Git 仓库并提交

**Files:**
- Create: `.gitignore`
- Modify: Git repository initialization

- [ ] **Step 1: 创建 .gitignore**
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env
*.log
```

- [ ] **Step 2: 初始化 Git 仓库并提交**
```bash
git init
git add .
git commit -m "feat: 初始天气机器人项目

- 添加天气服务（和风天气API）
- 添加消息生成器（个性化问候+吐槽）
- 添加企业微信推送客户端
- 添加定时调度器（每天早上6点）
- 项目结构：config.py, weather_service.py, message_generator.py, wechat_client.py, scheduler.py, main.py"
```

---

## 自检清单

- [ ] 所有文件路径正确
- [ ] 所有依赖包在 requirements.txt 中
- [ ] 代码无 placeholder（TODO、TBD等）
- [ ] 配置文件使用环境变量
- [ ] 消息格式符合设计文档

---

## 执行选择

**Plan complete and saved to `docs/superpowers/plans/2026-05-29-weather-robot-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
