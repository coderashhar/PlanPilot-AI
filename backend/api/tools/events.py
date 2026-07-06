from tavily import TavilyClient
from typing import List, Dict, Any
from api.config.settings import settings
from api.utils.logger import get_logger

logger = get_logger("events_tool")

def get_events(city: str) -> List[Dict[str, Any]]:
    """Get latest events about a city using Tavily"""
    if not settings.TAVILY_API_KEY:
        logger.warning("TAVILY_API_KEY is not set.")
        return []
        
    try:
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        response = client.search(
            query=f"latest events happening in {city} today or this weekend",
            search_depth="basic",
            max_results=3
        )
        
        results = response.get("results", [])
        events = []
        for r in results:
            events.append({
                "name": r.get("title", "Unknown Event"),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")
            })
        return events
    except Exception as e:
        logger.error(f"Failed to fetch events for {city}: {str(e)}")
        return []
