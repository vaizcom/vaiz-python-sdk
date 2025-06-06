# vaiz/models.py
from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Literal


class TaskFollower(RootModel):
    root: Dict[str, Literal["creator"]]


class CreateTaskRequest(BaseModel):
    name: str
    group: str
    board: str
    project: str
    creator: str
    followers: TaskFollower
    priority: int = 1
    hrid: Optional[str]
    completed: bool = False
    assignees: List[str] = []
    subtasks: List[str] = []
    milestones: List[str] = []
    customFields: List[str] = []
    types: List[str] = []
    rightConnectors: List[str] = []
    leftConnectors: List[str] = []
    document: Optional[str] = None


class TaskResponse(BaseModel):
    id: str
    name: str
    project: str
    board: str
    completed: bool
    # тут можно продолжать — в зависимости от того, что вернёт API