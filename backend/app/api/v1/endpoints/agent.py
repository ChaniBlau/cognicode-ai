from fastapi import APIRouter
from app.schemas.agent_schema import TaskRequest, TaskResponse
from app.agents.graph import app_graph

router = APIRouter()

@router.post("/generate", response_model=TaskResponse)
async def start_task(request: TaskRequest):
    # הרצת הגרף עם הקלט מהמשתמש
    initial_state = {
        "task": request.prompt,
        "plan": [],
        "code": "",
        "logs": []
    }
    
    result = app_graph.invoke(initial_state)
    
    return {
        "task_id": "unique-id-123",
        "status": "completed",
        "message": f"Plan created: {', '.join(result['plan'])}"
    }