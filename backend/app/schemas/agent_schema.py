from pydantic import BaseModel
from typing import List, Optional

class TaskRequest(BaseModel):
    prompt: str

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str