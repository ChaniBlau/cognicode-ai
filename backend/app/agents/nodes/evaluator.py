from app.agents.state import AgentState
from app.tools.sandbox import execute_code
import logging

logger = logging.getLogger(__name__)

def evaluator_node(state: AgentState):
    logger.info("--- EVALUATOR: TESTING CODE ---")
    code = state["code"]
    
    # כאן אפשר להוסיף לוגיקה שמזהה את השפה מהמשימה (לבינתיים נשתמש ב-python)
    result = execute_code(code, language="python")
    
    if result["success"]:
        return {
            "error": "", # ניקוי שגיאות קודמות
            "logs": ["Evaluator: Code executed successfully! Output: " + result["output"].strip()]
        }
    else:
        # עדכון השגיאה ב-State כדי שה-Coder ידע מה לתקן
        return {
            "error": result["error"],
            "logs": [f"Evaluator: Failed with error. Sending back to Coder."]
        }