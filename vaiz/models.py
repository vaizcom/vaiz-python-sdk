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


class EditTaskRequest(BaseModel):
    taskId: str
    name: Optional[str] = None
    parentTask: Optional[str] = None
    types: Optional[List[str]] = None
    priority: Optional[TaskPriority] = None
    completed: Optional[bool] = None
    assignees: Optional[List[str]] = None
    subtasks: Optional[List[str]] = None
    milestones: Optional[List[str]] = None
    dueStart: Optional[str] = None
    dueEnd: Optional[str] = None
    rightConnectors: Optional[List[str]] = None
    leftConnectors: Optional[List[str]] = None
    customFields: Optional[List[CustomField]] = None

    def dict(self, **kwargs):
        # Remove None values from the dict
        data = super().dict(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class Task(BaseModel):
    id: str
    name: str
    project: str
    board: str
    completed: bool


class TaskResponse(BaseModel):
    payload: Dict[str, Any]
    type: str