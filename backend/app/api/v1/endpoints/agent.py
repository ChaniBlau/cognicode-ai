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
            "language": "python", 
            "error": "",
            "logs": [f"Task started: {request.prompt}"],
            "iteration_count": 0,
            "search_query": "",   
            "context": ""       
        }

        # הרצת הגרף
        final_state = await app_graph.ainvoke(initial_state)

        is_failed = final_state.get("error") and final_state.get("iteration_count", 0) >= 3
        status = "failed" if is_failed else "completed"
        
        return TaskResponse(
            task_id=str(uuid.uuid4()),
            status=status,
            message="Process finished",
            plan=final_state.get("plan") or [],
            code=final_state.get("code") or "",
            logs=final_state.get("logs") or [],
            error=final_state.get("error") or ""   
        )
    except Exception as e:
        logger.error(f"Critical API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))