import requests
from typing import Dict, Any, Optional
from api.config.settings import settings
from api.utils.logger import get_logger

logger = get_logger("weather_tool")

def get_weather(city: str) -> Optional[Dict[str, Any]]:
    """Get current weather of a city"""
    if not settings.OPENWEATHERMAP_API_KEY:
        logger.warning("OPENWEATHERMAP_API_KEY is not set.")
        return None
        
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if str(data.get("cod")) != "200":
            logger.error(f"Weather API error: {data.get('message', 'Unknown error')}")
            return None
            
        return {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"]
        }
    except Exception as e:
        logger.error(f"Failed to fetch weather for {city}: {str(e)}")
        return None
