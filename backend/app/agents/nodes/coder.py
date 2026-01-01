import re
import logging
from app.agents.state import AgentState
from app.core.llm_factory import get_llm

logger = logging.getLogger(__name__)
llm = get_llm()

def coder_node(state: AgentState):
    logger.info("--- CODER: WRITING CODE (Multi-Language Support) ---")
    task = state["task"]
    plan = "\n".join(state["plan"])
    
    error_context = f"\nIMPORTANT: Previous attempt failed with this error: {state.get('error')}. Please fix it." if state.get("error") else ""

    prompt = f"""
    You are an expert polyglot programmer. Your task is to write high-quality, clean, and production-ready code.
    
    Task to solve: {task}
    Follow this logical plan:
    {plan}
    {error_context}

    Instructions:
    1. Determine the best programming language based on the task description (unless already specified).
    2. Return ONLY the source code.
    3. Do NOT include markdown blocks (like ```python or ```javascript) in your final response if possible, 
       but if you do, ensure the code is clearly enclosed.
    4. Do not provide explanations or comments outside the code.
    """

    response = llm.invoke(prompt)
    raw_content = response.content.strip()

    code_match = re.search(r"```(?:\w+\n)?(.*?)```", raw_content, re.DOTALL)
    if code_match:
        refined_code = code_match.group(1).strip()
    else:
        refined_code = raw_content

    return {
        "code": refined_code,
        "logs": ["Coder: Code generated/updated based on the provided plan."],
        "iteration_count": state.get("iteration_count", 0) + 1
    }