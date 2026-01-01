from app.agents.state import AgentState
from app.core.llm_factory import get_llm
import json
import re
import logging

logger = logging.getLogger(__name__)

llm = get_llm()

def architect_node(state: AgentState):
    logger.info("--- ARCHITECT: GENERATING PLAN ---")
    task = state["task"]

    prompt = f"""
Analyze the following task and return ONLY a VALID JSON array of logical steps.
Each step must be a short, clear sentence.
If unsure, still return a JSON array of strings.
Do NOT include markdown, explanations, or extra text.

Task:
{task}
"""

    response = llm.invoke(prompt)
    raw_content = response.content.strip()

    if raw_content.startswith("```") and raw_content.endswith("```"):
        raw_content = "\n".join(raw_content.split("\n")[1:-1]).strip()

    try:
        plan_steps = json.loads(raw_content)
        if not isinstance(plan_steps, list):
            logger.error("Parsed JSON is not a list")
            raise ValueError("Parsed JSON is not a list")
    except (json.JSONDecodeError, ValueError):
        plan_steps = [
            re.sub(r'^\d+\.\s*', '', line.strip())  
            for line in raw_content.split("\n")
            if line.strip() and not line.strip().startswith("-") and len(line.strip()) > 3
        ]

    return {
        "plan": plan_steps,
        "logs": [f"Architect: Generated {len(plan_steps)} steps."]
    }
