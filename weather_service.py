import requests
from config import config

class WeatherService:
    def __init__(self):
        self.api_key = config.HEFENG_API_KEY
        self.api_host = config.HEFENG_API_HOST
        self.city = config.CITY

    def get_weather(self, city=None):
        url = f"https://{self.api_host}/v7/weather/now"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(city),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_weather_data(data)

    def get_daily_forecast(self, city=None):
        url = f"https://{self.api_host}/v7/weather/3d"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(city),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_forecast_data(data, city)

    def get_hourly_forecast(self, city=None):
        url = f"https://{self.api_host}/v7/weather/24h"
        params = {
            "key": self.api_key,
            "location": self._get_location_code(city),
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("code") != "200":
            raise Exception(f"Weather API error: {data.get('code')}, message: {data.get('message')}")

        return self._parse_hourly_data(data)

    def _get_precip_prob(self, city=None):
        try:
            hourly_data = self.get_hourly_forecast(city)
            if hourly_data and len(hourly_data) > 0:
                return hourly_data[0].get("precip_prob", "0")
        except:
            pass
        return "0"

    def _get_location_code(self, city=None):
        target_city = city or self.city
        
        # 预设常用城市代码映射
        city_codes = {
            "北京": "101010100",
            "上海": "101020100",
            "天津": "101030100",
            "重庆": "101040100",
            "哈尔滨": "101050101",
            "长春": "101060101",
            "沈阳": "101070101",
            "呼和浩特": "101080101",
            "石家庄": "101090101",
            "太原": "101100101",
            "西安": "101110101",
            "济南": "101120101",
            "乌鲁木齐": "101130101",
            "拉萨": "101140101",
            "西宁": "101150101",
            "兰州": "101160101",
            "银川": "101170101",
            "郑州": "101180101",
            "南京": "101190101",
            "杭州": "101210101",
            "宁波": "101210401",
            "合肥": "101220101",
            "福州": "101230101",
            "南昌": "101240101",
            "长沙": "101250101",
            "武汉": "101200101",
            "成都": "101270101",
            "贵阳": "101260101",
            "昆明": "101290101",
            "广州": "101280101",
            "深圳": "101280601",
            "南宁": "101300101",
            "海口": "101310101",
            "香港": "101320101",
            "澳门": "101330101",
            "台北": "101340101"
        }
        
        if target_city in city_codes:
            return city_codes[target_city]
            
        # 如果预设中没有，则调用 GeoAPI 动态查询
        try:
            geo_url = "https://geoapi.qweather.com/v2/city/lookup"
            params = {
                "key": self.api_key,
                "location": target_city
            }
            response = requests.get(geo_url, params=params, timeout=10)
            data = response.json()
            if data.get("code") == "200" and data.get("location"):
                return data["location"][0]["id"]
        except Exception as e:
            print(f"GeoAPI error for {target_city}: {e}")
            
        return "101020100"  # 默认返回上海

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

    def _parse_forecast_data(self, data, city=None):
        daily = data.get("daily", [])[0] if data.get("daily") else {}
        return {
            "temp_max": daily.get("tempMax"),
            "temp_min": daily.get("tempMin"),
            "precip_prob": self._get_precip_prob(city),
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
