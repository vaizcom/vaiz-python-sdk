# vaiz/models.py
from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Literal, Any


class TaskFollower(RootModel):
    root: Dict[str, Literal["creator"]]


class CreateTaskRequest(BaseModel):
    name: str
    group: str
    board: str
    project: str
    parentTask: Optional[str] = None
    types: List[str] = []
    priority: int = 1
    completed: bool = False
    assignees: List[str] = []
    subtasks: List[str] = []
    milestones: List[str] = []
    dueStart: Optional[str] = None
    dueEnd: Optional[str] = None
    rightConnectors: List[str] = []
    leftConnectors: List[str] = []
    customFields: List[str] = []


class Task(BaseModel):
    id: str
    name: str
    project: str
    board: str
    completed: bool


class TaskResponse(BaseModel):
    payload: Dict[str, Any]
    type: str