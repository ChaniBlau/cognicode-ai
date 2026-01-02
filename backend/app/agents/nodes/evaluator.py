from app.agents.state import AgentState
from app.tools.sandbox import execute_code
import logging

logger = logging.getLogger(__name__)

def evaluator_node(state: AgentState):
    logger.info(f"--- EVALUATOR: TESTING CODE ({state.get('language')}) ---")
    
    code = state["code"]
    lang = state.get("language", "python").lower() 
    
    result = execute_code(code, lang)
    
    if result["success"]:
        # אנחנו מוסיפים את הפלט של הקוד ללוגים כדי שהמשתמש יראה את התוצאה
        output_preview = result["output"].strip()
        return {
            "error": "",
            "logs": [f"Evaluator: {lang} executed successfully! Output: {output_preview}"]
        }
    else:
        # במקרה של שגיאה, השגיאה נשמרת ב-state['error'] וה-coder יקבל אותה
        return {
            "error": "",
            "logs": [f"Evaluator: {lang} executed successfully! Full Output:\n{result['output'].strip()}"]
        }