from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.architect import architect_node
from app.agents.nodes.coder import coder_node
from app.agents.nodes.evaluator import evaluator_node # ייבוא חדש

def decide_next_step(state: AgentState):

    if not state.get("error"):
        return END
    
    if state.get("iteration_count", 0) < 3:
        return "coder"
    
    return END

def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("evaluator", evaluator_node)

    workflow.set_entry_point("architect")
    workflow.add_edge("architect", "coder")
    workflow.add_edge("coder", "evaluator")

    workflow.add_conditional_edges(
        "evaluator",
        decide_next_step,
        {
            "coder": "coder", 
            END: END          
        }
    )

    return workflow.compile()

app_graph = create_graph()