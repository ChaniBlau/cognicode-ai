from fastapi import APIRouter, HTTPException
from app.schemas.agent_schema import TaskRequest, TaskResponse
from app.agents.graph import app_graph
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", response_model=TaskResponse)
async def start_task(request: TaskRequest):
    try:
        logger.info(f"Starting task: {request.prompt}")

        initial_state = {
            "task": request.prompt,
            "plan": [],
            "code": "",
            "logs": [f"Task started: {request.prompt}"]
        }

        final_state = await app_graph.ainvoke(initial_state)

        return TaskResponse(
            task_id=str(uuid.uuid4()),
            status="completed",
            message="Plan generated successfully",
            plan=final_state["plan"],
            code=final_state["code"]
        )
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
