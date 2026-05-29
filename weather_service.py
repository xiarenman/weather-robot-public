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
