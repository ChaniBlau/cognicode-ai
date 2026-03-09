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
    search_query: str = Field(description="If you need more info to solve the task, provide a search query. Otherwise, leave empty.")

def architect_node(state: AgentState):
    logger.info("--- ARCHITECT: GENERATING PLAN ---")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(ArchitectResponse)

    prompt = f"""
    You are a Senior Software Architect. Analyze the task and determine the best execution environment.
    USER TASK: {state['task']}
    """

    try:
        response = structured_llm.invoke(prompt)
        return {
            "language": response.language,
            "plan": response.plan,
            "search_query": response.search_query or "", # חייב להופיע כאן!
            "logs": [f"Architect: Selected {response.language}."] # חייב להיות רשימה []
        }
    except Exception as e:
        logger.error(f"Architect Error: {e}")
        return {
            "language": "python",
            "plan": ["Emergency fallback plan"],
            "search_query": "", # גם במקרה של שגיאה, מחזירים ערך ריק
            "logs": [f"Architect Error: {str(e)}"]
        }