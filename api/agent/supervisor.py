from langgraph.graph import StateGraph, END
from api.agent.state import AgentState
from api.agent.nodes.intent import extract_intent
from api.agent.nodes.tools import execute_tools
from api.agent.nodes.scoring import score_and_respond
from api.utils.logger import get_logger

logger = get_logger("supervisor")

def compile_graph():
    logger.info("Compiling LangGraph StateGraph...")
    workflow = StateGraph(AgentState)
    
    workflow.add_node("intent", extract_intent)
    workflow.add_node("tools", execute_tools)
    workflow.add_node("scoring", score_and_respond)
    
    workflow.set_entry_point("intent")
    workflow.add_edge("intent", "tools")
    workflow.add_edge("tools", "scoring")
    workflow.add_edge("scoring", END)
    
    return workflow.compile()

graph = compile_graph()
