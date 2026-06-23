from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models.schemas import UserRequest, AgentResponse
from api.agent.supervisor import graph
from api.utils.logger import get_logger

logger = get_logger("fastapi")

app = FastAPI(title="PlanPilot AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=AgentResponse)
async def chat_endpoint(request: UserRequest):
    logger.info(f"Received query: {request.query}")
    try:
        # Initialize state
        initial_state = {
            "query": request.query,
            "intent": "",
            "location": "",
            "weather_data": None,
            "places_data": [],
            "events_data": [],
            "response": None
        }
        
        # Invoke LangGraph
        result = graph.invoke(initial_state)
        
        # Extract response
        if "response" in result and result["response"]:
            return result["response"]
        else:
            raise HTTPException(status_code=500, detail="Agent failed to generate a response")
            
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
