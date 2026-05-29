import random
from datetime import datetime
from config import config

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
    def generate(self, weather_data, forecast_data, city=None):
        greeting = random.choice(GREETINGS)
        complaint = random.choice(WEATHER_COMPLAINTS)
        
        display_city = city or config.CITY

        temp = int(weather_data["temp"])
        feels_like = weather_data["feels_like"]
        humidity = weather_data["humidity"]
        wind_dir = weather_data["wind_dir"]
        wind_scale = weather_data["wind_scale"]
        weather_text = weather_data["weather_text"]

        temp_max = int(forecast_data["temp_max"])
        temp_min = int(forecast_data["temp_min"])
        precip_prob = int(forecast_data["precip_prob"])

        today = datetime.now()
        date_str = today.strftime("%Y年%m月%d日")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()]

        clothing = self._get_clothing_advice(temp, weather_text)
        umbrella = self._get_umbrella_advice(precip_prob)

        message = f"""☀️ {display_city}今日天气（{date_str} {weekday}）

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
