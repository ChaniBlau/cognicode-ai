from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.architect import architect_node

def create_graph():
    # 1. מגדירים גרף שעובד עם ה-State שלנו
    workflow = StateGraph(AgentState)

    # 2. מוסיפים את ה-Nodes (הפעולות)
    workflow.add_node("architect", architect_node)

    # 3. מגדירים את הקישורים (Edges)
    workflow.set_entry_point("architect") # מאיפה מתחילים?
    workflow.add_edge("architect", END)     # לאן ממשיכים? (כרגע ישר לסוף)

    # 4. מקמפלים את הגרף
    return workflow.compile()

# יצירת מופע של הגרף להרצה
app_graph = create_graph()