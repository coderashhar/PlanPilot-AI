from typing import TypedDict, List, Dict, Any, Optional
from api.models.schemas import AgentResponse

class AgentState(TypedDict):
    query: str
    intent: str
    location: str
    required_tools: List[str]
    
    # Raw data from tools
    weather_data: Optional[Dict[str, Any]]
    places_data: List[Dict[str, Any]]
    events_data: List[Dict[str, Any]]
    
    # Processed output
    response: Optional[AgentResponse]
