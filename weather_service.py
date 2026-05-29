import requests
from config import config

class WeatherService:
    def __init__(self):
        self.api_key = config.HEFENG_API_KEY
        self.api_host = config.HEFENG_API_HOST
        self.city = config.CITY

    def get_weather(self):
        url = f"https://{self.api_host}/v7/weather/now"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_weather_data(data)

    def get_daily_forecast(self):
        url = f"https://{self.api_host}/v7/weather/3d"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_forecast_data(data)

    def get_hourly_forecast(self):
        url = f"https://{self.api_host}/v7/weather/24h"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_hourly_data(data)

    def _get_precip_prob(self):
        try:
            hourly_data = self.get_hourly_forecast()
            if hourly_data and len(hourly_data) > 0:
                return hourly_data[0].get("precip_prob", "0")
        except:
            pass
        return "0"

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
            "precip_prob": self._get_precip_prob(),
        }

    def _parse_hourly_data(self, data):
        hourly_list = data.get("hourly", [])
        result = []
        for hour in hourly_list:
            result.append({
                "time": hour.get("fxTime"),
                "temp": hour.get("temp"),
                "precip_prob": hour.get("pop"),
                "weather_text": hour.get("text"),
            })
        return result

weather_service = WeatherService()
