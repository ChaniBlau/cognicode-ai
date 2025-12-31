from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # ההודעה המקורית מהמשתמש
    task: str
    # רשימת התוכניות/שלבים שהארכיטקט תכנן
    plan: List[str]
    # הקוד הנוכחי שנכתב
    code: str
    # רשימת לוגים או שגיאות שקרו בדרך
    logs: Annotated[List[str], operator.add]