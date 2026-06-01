from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from config import config
from weather_service import weather_service
from message_generator import message_generator
from wechat_client import wechat_client

def send_daily_weather():
    # 兼容中英文逗号，并过滤空字符串
    raw_cities = config.CITY.replace("，", ",")
    cities = [c.strip() for c in raw_cities.split(",") if c.strip()]
    
    for city in cities:
        try:
            print(f"Fetching weather for {city}...")
            weather_data = weather_service.get_weather(city)
            forecast_data = weather_service.get_daily_forecast(city)
            message = message_generator.generate(weather_data, forecast_data, city)
            
            # 优先使用 Webhook 发送（支持多个 Webhook）
            if config.WECOM_WEBHOOK_URL:
                webhooks = [url.strip() for url in config.WECOM_WEBHOOK_URL.replace("，", ",").split(",") if url.strip()]
                for url in webhooks:
                    wechat_client.send_webhook_message(message, webhook_url=url)
                    print(f"Weather message for {city} sent via Webhook successfully at {datetime.now()}")
            else:
                wechat_client.send_message(message)
                print(f"Weather message for {city} sent via App successfully at {datetime.now()}")
        except Exception as e:
            print(f"Failed to send weather message for {city}: {e}")
            # 如果是最后一个城市报错，仍然抛出异常以通知 GitHub Actions
            if city == cities[-1]:
                raise e

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
    send_daily_weather()
