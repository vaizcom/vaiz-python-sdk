# vaiz/models.py
from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Literal, Any, Union
from enum import Enum


class TaskFollower(RootModel):
    root: Dict[str, Literal["creator"]]


class TaskPriority(int, Enum):
    Low = 0
    General = 1
    Medium = 2
    High = 3


class CustomField(BaseModel):
    id: str
    value: Union[str, List[str]]


class CreateTaskRequest(BaseModel):
    name: str
    group: str
    board: str
    project: str
    parentTask: Optional[str] = None
    types: List[str] = []
    priority: TaskPriority = TaskPriority.General
    completed: bool = False
    assignees: List[str] = []
    subtasks: List[str] = []
    milestones: List[str] = []
    dueStart: Optional[str] = None
    dueEnd: Optional[str] = None
    rightConnectors: List[str] = []
    leftConnectors: List[str] = []
    customFields: List[CustomField] = []


class Task(BaseModel):
    id: str
    name: str
    project: str
    board: str
    completed: bool


class TaskResponse(BaseModel):
    payload: Dict[str, Any]
    type: str