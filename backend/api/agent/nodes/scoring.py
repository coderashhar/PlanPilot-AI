from api.agent.state import AgentState
from api.models.schemas import AgentResponse, Recommendation, WeatherData, EventData
from api.utils.logger import get_logger

logger = get_logger("scoring_node")

def score_and_respond(state: AgentState) -> AgentState:
    """Applies dynamic intent-aware deterministic scoring to generate recommendations"""
    logger.info("Scoring and generating response...")
    
    intent = state.get("intent", "").lower()
    places_data = state.get("places_data", [])
    weather_data = state.get("weather_data")
    events_data = state.get("events_data", [])
    
    # 1. Define profiles (Weights: [Rating, Price, Weather Suitability])
    weights = {"rating": 0.5, "price": 0.2, "weather": 0.3} # default
    if "food" in intent or "eat" in intent or "dinner" in intent:
        weights = {"rating": 0.7, "price": 0.2, "weather": 0.1}
    elif "rain" in intent or "indoor" in intent:
        weights = {"rating": 0.4, "price": 0.1, "weather": 0.5}
    elif "birthday" in intent or "celebration" in intent:
        weights = {"rating": 0.6, "price": 0.4, "weather": 0.0}
        
    logger.info(f"Using scoring weights: {weights}")
    
    recommendations = []
    
    for place in places_data:
        # Base rating score (rating/5 * 100)
        rating_score = (place.get("rating", 3.0) / 5.0) * 100
        
        # Price score
        raw_price_level = place.get("price_level")
        price_level = raw_price_level if raw_price_level is not None else 2
        price_score = 100 - (abs(2 - price_level) * 20)
        
        # Cost mapping
        cost = price_level * 500 if raw_price_level is not None else None
        
        # URL formatting
        place_id = place.get("place_id")
        place_url = None
        if place_id:
            import urllib.parse
            encoded_name = urllib.parse.quote(place.get("name", "Unknown"))
            place_url = f"https://www.google.com/maps/search/?api=1&query={encoded_name}&query_place_id={place_id}"
        
        # Weather score
        weather_score = 80 # default
        if weather_data and "rain" in str(weather_data.get("condition", "")).lower():
            if "park" in str(place.get("types", [])):
                weather_score = 20
                
        final_score = (rating_score * weights["rating"]) + (price_score * weights["price"]) + (weather_score * weights["weather"])
        
        recommendations.append(
            Recommendation(
                name=place.get("name", "Unknown"),
                score=round(final_score, 1),
                estimated_cost=cost,
                reason=f"Selected based on {intent} profile. Rating: {place.get('rating')}",
                url=place_url
            )
        )
        
    # Sort recommendations by score descending
    recommendations.sort(key=lambda x: x.score, reverse=True)
    
    # Format WeatherData
    weather_model = None
    if weather_data:
        weather_model = WeatherData(
            condition=weather_data.get("condition", ""),
            temperature=weather_data.get("temperature", 0.0)
        )
        
    # Format EventData
    event_models = []
    for event in events_data:
        event_models.append(
            EventData(
                name=event.get("name", ""),
                time="Today", # Mocked
                location=event.get("url", "")
            )
        )
        
    response = AgentResponse(
        weather=weather_model,
        recommendations=recommendations[:3], # Return top 3
        events=event_models[:3],
        summary=f"Here are the best options for your {intent} in {state.get('location', 'the area')}."
    )
    
    return {"response": response}
