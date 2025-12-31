from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.agents.state import AgentState
import os

# אתחול המודל (ChatOpenAI ימשוך את המפתח אוטומטית מה-env)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def architect_node(state: AgentState):
    print("--- ARCHITECT: Thinking with AI ---")
    task = state["task"]
    
    # הפרומפט שינחה את הארכיטקט
    system_prompt = (
        "You are an expert Software Architect. "
        "Create a concise technical plan (3-5 steps) to solve the user's task. "
        "Return only the steps, separated by newlines."
    )
    
    # קריאה ל-OpenAI
    response = model.invoke([
        HumanMessage(content=f"{system_prompt}\n\nTask: {task}")
    ])
    
    # הפיכת התשובה לרשימה (Plan)
    plan_steps = response.content.strip().split("\n")
    
    return {
        "plan": plan_steps,
        "logs": [f"Architect generated a plan with {len(plan_steps)} steps."]
    }