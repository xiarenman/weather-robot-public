import requests
import jwt
import time
from pathlib import Path
from config import config

class WeatherService:
    def __init__(self):
        self.key_id = config.HEFENG_KEY_ID
        self.private_key_path = config.HEFENG_PRIVATE_KEY_PATH
        self.city = config.CITY
        self._token = None
        self._token_expires = 0

    def _get_token(self):
        if self._token and time.time() < self._token_expires:
            return self._token

        private_key = Path(self.private_key_path).read_text()

        payload = {
            "iss": self.key_id,
            "exp": int(time.time()) + 3600,
            "iat": int(time.time()),
        }

        self._token = jwt.encode(payload, private_key, algorithm="EdDSA")
        self._token_expires = int(time.time()) + 3500
        return self._token

    def get_weather(self):
        url = f"https://devapi.qweather.com/v7/weather/now"
        params = {
            "location": self._get_location_code(),
        }
        headers = {"Authorization": f"Bearer {self._get_token()}"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_weather_data(data)

    def get_daily_forecast(self):
        url = f"https://devapi.qweather.com/v7/weather/3d"
        params = {
            "location": self._get_location_code(),
        }
        headers = {"Authorization": f"Bearer {self._get_token()}"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

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
