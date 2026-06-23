from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List
from api.agent.state import AgentState
from api.config.settings import settings
from api.utils.logger import get_logger

logger = get_logger("intent_node")

class IntentOutput(BaseModel):
    intent: str = Field(description="The primary intent of the user (e.g., food discovery, birthday celebration, date night, weekend outing, tourism, rainy-day plan, family outing)")
    location: str = Field(description="The city or location mentioned in the query. Extract the city name.")
    required_tools: List[str] = Field(description="List of tools needed to answer this query. Options: ['weather', 'places', 'events']. E.g., if user only asks for food, select ['places']. If they ask for events, select ['events']. If they ask for outdoor plans, select ['weather', 'places'].")

def extract_intent(state: AgentState) -> AgentState:
    """Extracts the user intent, location, and required tools from the query"""
    logger.info("Extracting intent, location, and tools...")
    
    if not settings.GOOGLE_API_KEY:
        logger.warning("GOOGLE_API_KEY is missing. Using fallback intent.")
        return {"intent": "general outing", "location": "Bhopal", "required_tools": ["weather", "places", "events"]}

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=settings.GOOGLE_API_KEY)
        structured_llm = llm.with_structured_output(IntentOutput)
        
        prompt = PromptTemplate.from_template(
            "Analyze the following user request and determine their primary intent, the city/location, and which tools are strictly necessary.\n\nUser Request: {query}\n\nOutput:"
        )
        
        chain = prompt | structured_llm
        result = chain.invoke({"query": state["query"]})
        
        logger.info(f"Detected intent: {result.intent}, Location: {result.location}, Tools: {result.required_tools}")
        return {"intent": result.intent, "location": result.location, "required_tools": result.required_tools}
    except Exception as e:
        logger.error(f"Failed to extract intent: {str(e)}")
        return {"intent": "general outing", "location": "Bhopal"}
