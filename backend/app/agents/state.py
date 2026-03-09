from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    task: str
    plan: List[str]
    code: str
    language: str  
    error: str
    logs: Annotated[List[str], operator.add]
    iteration_count: int  
    search_query: str 
    context: str