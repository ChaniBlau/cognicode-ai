from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.architect import architect_node
from app.agents.nodes.coder import coder_node

def create_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)

    workflow.set_entry_point("architect")
    workflow.add_edge("architect", "coder")

    workflow.add_edge("coder", END)

    return workflow.compile()

app_graph = create_graph()