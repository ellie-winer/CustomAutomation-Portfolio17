import requests
from datetime import datetime, timezone
from typing import Dict, Any

import config

def get_location_by_ip() -> Dict[str, Any]:
    if config.IP_GEOLOCATION_PROVIDER == "ip-api":
        resp = requests.get("http://ip-api.com/json/")
        resp.raise_for_status()
        data = resp.json()
        return {
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "timezone": data.get("timezone"),
        }
    else:
        raise RuntimeError("Unsupported geolocation provider: " + config.IP_GEOLOCATION_PROVIDER)


def fetch_current_weather(lat: float, lon: float) -> Dict[str, Any]:

    if not config.OPENWEATHERMAP_API_KEY:
        raise RuntimeError("OpenWeatherMap API key is not set in config.py")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": config.OPENWEATHERMAP_API_KEY,
        "units": config.UNITS,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def categorize_weather(weather_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    takes OpenWeatherMap response and returns a dictionary
    """
    main = None
    description = None
    temp = None

    weather_list = weather_json.get("weather", [])
    if weather_list:
        main = weather_list[0].get("main", "")
        description = weather_list[0].get("description", "")
    main_weather = main or ""
    description = description or ""

    main_data = weather_json.get("main", {})
    temp = main_data.get("temp")

    categories = set()

    # precipitation categories broken down
    main_lower = main_weather.lower()
    desc_lower = description.lower()

    if "rain" in main_lower or "drizzle" in main_lower or "shower" in desc_lower:
        categories.add("rainy")
    if "thunder" in main_lower or "thunderstorm" in desc_lower:
        categories.add("storm")
    if "snow" in main_lower or "sleet" in main_lower:
        categories.add("snow")
    if "clear" in main_lower:
        categories.add("sunny")
    if "cloud" in main_lower or "overcast" in desc_lower:
        categories.add("cloudy")
    if "mist" in main_lower or "fog" in main_lower or "haze" in main_lower:
        categories.add("foggy")

    # temperature categories broken down
    if temp is not None:
        try:
            temp_val = float(temp)
            if temp_val >= config.HOT_THRESHOLD:
                categories.add("hot")
            elif temp_val <= config.COLD_THRESHOLD:
                categories.add("cold")
            else:
                categories.add("mild")
        except (ValueError, TypeError):
            categories.add("unknown_temp")
    else:
        categories.add("unknown_temp")


    categories.add(main_weather.lower())

    return {
        "main": main_weather,
        "description": description,
        "temp": temp,
        "categories": sorted(categories),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
