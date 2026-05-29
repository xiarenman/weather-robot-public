from scheduler import send_daily_weather

if __name__ == "__main__":
    print("Starting Weather Robot (Cloud Run)...")
    send_daily_weather()
    print("Weather Robot finished successfully.")
