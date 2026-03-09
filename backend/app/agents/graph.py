from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.architect import architect_node
from app.agents.nodes.coder import coder_node
from app.agents.nodes.evaluator import evaluator_node
from app.agents.nodes.researcher import researcher_node  # ייבוא של החוקר החדש

def router_after_architect(state: AgentState):
    # שימוש ב-.get() עם ברירת מחדל למניעת קריסה
    query = state.get("search_query", "")
    if query and len(query.strip()) > 0:
        return "researcher"
    return "coder"

def decide_next_step(state: AgentState):
    """
    מחליט אם לסיים או לנסות לתקן את הקוד.
    """
    if not state.get("error"):
        return END
    
    if state.get("iteration_count", 0) < 3:
        return "coder"
    
    return END

def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("architect", architect_node)
    workflow.add_node("researcher", researcher_node) # הצומת החדש
    workflow.add_node("coder", coder_node)
    workflow.add_node("evaluator", evaluator_node)

    workflow.set_entry_point("architect")

    workflow.add_conditional_edges(
        "architect",
        router_after_architect,
        {
            "researcher": "researcher",
            "coder": "coder"
        }
    )

    workflow.add_edge("researcher", "coder")
    
    workflow.add_edge("coder", "evaluator")

    workflow.add_conditional_edges(
    "evaluator",
    decide_next_step,
    {
        "coder": "coder", 
        END: END  # שימוש באובייקט END עצמו
    }
)

    return workflow.compile()

app_graph = create_graph()