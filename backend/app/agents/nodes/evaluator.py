from app.agents.state import AgentState
from app.tools.sandbox import execute_code
import logging

logger = logging.getLogger(__name__)

def evaluator_node(state: AgentState):
    """
   checks the code for compilation and runtime errors by executing it in a sandboxed environment.
    """
    logger.info(f"--- EVALUATOR: TESTING CODE ({state.get('language')}) ---")
    
    # שליפת נתונים מה-State
    code = state.get("code", "")
    lang = state.get("language", "python").lower() 
    
    # הרצת הקוד בסנדבוקס
    result = execute_code(code, lang)
    
    # מקרה 1: הצלחה - הקוד רץ ללא שגיאות
    if result.get("success"):
        output_preview = result.get("output", "").strip()
        logger.info("Evaluator: Success")
        
        return {
            "error": "", # מנקים שגיאות קודמות אם היו
            "logs": [f"Evaluator: {lang} executed successfully! Output: {output_preview}"]
        }
    
    # מקרה 2: כישלון - נמצאה שגיאת קומפילציה או הרצה
    else:
        # שליפת הודעת השגיאה מהסנדבוקס (מפתח 'error')
        error_msg = result.get("error", "Unknown execution error").strip()
        
        # עדכון מונה הנסיונות כדי למנוע לולאה אינסופית
        current_iteration = state.get("iteration_count", 0) + 1
        
        logger.warning(f"Evaluator: Failed on attempt {current_iteration}")
        
        return {
            "error": error_msg,
            "iteration_count": current_iteration,
            "logs": [f"Evaluator: {lang} failed. Attempt {current_iteration}/3. Error: {error_msg}"]
        }