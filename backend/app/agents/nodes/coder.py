import re
import logging
from app.agents.state import AgentState
from app.core.llm_factory import get_llm

logger = logging.getLogger(__name__)

def coder_node(state: AgentState):
    """
    סוכן הכתיבה: מייצר קוד בשפה שנבחרה על ידי הארכיטקט.
    """
    logger.info(f"--- CODER: WRITING CODE (Target Language: {state.get('language')}) ---")
    
    llm = get_llm()
    task = state["task"]
    plan = "\n".join(state["plan"])
    language = state.get("language", "python") 
    
    error_context = ""
    if state.get("error"):
        error_context = f"""
        ---
        PREVIOUS ERROR DETECTED:
        {state.get('error')}
        Please analyze the error and fix the code accordingly.
        ---
        """

    prompt = f"""
    You are an expert Senior Developer specializing in {language}.
    
    Task: {task}
    Selected Language: {language}
    
    Follow this implementation plan:
    {plan}
    {error_context}

    CRITICAL INSTRUCTIONS:
    1. Write ONLY valid {language} code.
    2. Ensure the code is production-ready, clean, and follows {language} best practices.
    3. MANDATORY: Include an example usage at the end that prints the result to the console 
       (e.g., use 'print()' for Python, 'console.log()' for JavaScript, etc.) so we can verify the output.
    4. Return ONLY the code. No explanations, no markdown introduction, no comments outside the code.
    """

    response = llm.invoke(prompt)
    raw_content = response.content.strip()


    code_match = re.search(r"```(?:\w+)?\n?(.*?)```", raw_content, re.DOTALL)
    if code_match:
        refined_code = code_match.group(1).strip()
    else:
        refined_code = raw_content.replace("```", "").strip()

    return {
        "code": refined_code,
        "logs": [f"Coder: Successfully generated {language} code."],
        "iteration_count": state.get("iteration_count", 0) + 1
    }