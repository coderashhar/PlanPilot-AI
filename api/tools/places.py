import requests
from typing import List, Dict, Any
from api.config.settings import settings
from api.utils.logger import get_logger

logger = get_logger("places_tool")

def search_places(query: str, location: str = "") -> List[Dict[str, Any]]:
    """Search for places using Google Places API Text Search"""
    if not settings.GOOGLE_PLACES_API_KEY:
        logger.warning("GOOGLE_PLACES_API_KEY is not set.")
        return []
        
    search_query = f"{query} in {location}" if location else query
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&key={settings.GOOGLE_PLACES_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") not in ["OK", "ZERO_RESULTS"]:
            logger.error(f"Places API error: {data.get('status')} - {data.get('error_message', '')}")
            return []
            
        results = data.get("results", [])[:5] # Limit to top 5
        places = []
        for r in results:
            places.append({
                "name": r.get("name"),
                "rating": r.get("rating", 0.0),
                "price_level": r.get("price_level", 0),
                "address": r.get("formatted_address"),
                "types": r.get("types", [])
            })
        return places
    except Exception as e:
        logger.error(f"Failed to fetch places for {search_query}: {str(e)}")
        return []
