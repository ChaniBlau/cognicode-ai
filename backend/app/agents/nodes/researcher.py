from app.agents.state import AgentState
from app.tools.search import search_web
import logging

logger = logging.getLogger(__name__)

def researcher_node(state: AgentState):
    query = state.get("search_query") or state.get("task")
    
    # הרצת החיפוש (שעכשיו מוגן מפני קריסה)
    search_results = search_web(query)
    
    return {
        "context": search_results,
        "logs": ["Researcher: Attempted search, added results/warnings to context."]
    }