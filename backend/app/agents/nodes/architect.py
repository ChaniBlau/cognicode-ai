from app.agents.state import AgentState
from app.core.llm_factory import get_llm
from pydantic import BaseModel, Field
from typing import List, Literal
import logging

logger = logging.getLogger(__name__)

class ArchitectResponse(BaseModel):
    language: Literal["python", "nodejs", "javascript", "go", "java", "cpp"] = Field(
        description="The specific runtime environment or language required."
    )
    plan: List[str] = Field(min_items=1, description="Detailed step-by-step implementation plan.")

def architect_node(state: AgentState):
    logger.info("--- ARCHITECT: GENERATING PLAN ---")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(ArchitectResponse)

    prompt = f"""
    You are a Senior Software Architect. Analyze the task and determine the best execution environment.
    
    GUIDELINES:
    - If the user asks for 'NodeJS' or backend JS, set language to 'nodejs'.
    - If the user asks for 'browser' or generic JS, set language to 'javascript'.
    - Provide a technical, granular plan.

    USER TASK:
    {state['task']}
    """

    try:
        response = structured_llm.invoke(prompt)
        return {
            "language": response.language,
            "plan": response.plan,
            "logs": [f"Architect: Selected {response.language}. Plan includes {len(response.plan)} steps."]
        }
    except Exception as e:
        logger.error(f"Architect Error: {e}")
        return {
            "language": "python",
            "plan": ["Process the request using Python standard library"],
            "logs": ["Architect: Error in structured output, falling back to Python."]
        }