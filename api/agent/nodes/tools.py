from api.agent.state import AgentState
from api.tools.weather import get_weather
from api.tools.places import search_places
from api.tools.events import get_events
from api.utils.logger import get_logger

logger = get_logger("tools_node")

def execute_tools(state: AgentState) -> AgentState:
    """Executes necessary tools based on the query, with fallback logic"""
    logger.info("Executing tools...")
    query = state["query"]
    location = state.get("location", "Bhopal")
    required_tools = state.get("required_tools", ["weather", "places", "events"])
    
    weather_data = None
    places_data = []
    events_data = []
    
    # 1. Weather
    if "weather" in required_tools:
        logger.info(f"Fetching weather for {location}...")
        weather_data = get_weather(location) 
    
    # 2. Places
    if "places" in required_tools:
        logger.info(f"Fetching places for '{query}' in {location}...")
        places_data = search_places(query, location)
    
    # 3. Events
    if "events" in required_tools:
        logger.info(f"Fetching events for {location}...")
        events_data = get_events(location)
    
    return {
        "weather_data": weather_data,
        "places_data": places_data,
        "events_data": events_data
    }
