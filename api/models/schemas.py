from pydantic import BaseModel, Field
from typing import List, Optional

class UserRequest(BaseModel):
    query: str
    
class Recommendation(BaseModel):
    name: str
    score: float
    estimated_cost: Optional[float] = None
    reason: str
    
class WeatherData(BaseModel):
    condition: str
    temperature: float
    
class EventData(BaseModel):
    name: str
    time: str
    location: Optional[str] = None
    
class AgentResponse(BaseModel):
    weather: Optional[WeatherData] = None
    recommendations: List[Recommendation] = Field(default_factory=list)
    events: List[EventData] = Field(default_factory=list)
    summary: str
