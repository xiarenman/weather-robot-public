from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from config import config
from weather_service import weather_service
from message_generator import message_generator
from wechat_client import wechat_client

def send_daily_weather():
    try:
        weather_data = weather_service.get_weather()
        forecast_data = weather_service.get_daily_forecast()
        message = message_generator.generate(weather_data, forecast_data)
        
        # 优先使用 Webhook 发送
        if config.WECOM_WEBHOOK_URL:
            wechat_client.send_webhook_message(message)
            print(f"Weather message sent via Webhook successfully at {datetime.now()}")
        else:
            wechat_client.send_message(message)
            print(f"Weather message sent via App successfully at {datetime.now()}")
    except Exception as e:
        print(f"Failed to send weather message: {e}")
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
