from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import TaskPriority, CustomField


class TaskCustomField(BaseModel):
    id: str
    value: Any
    _id: str


class Task(BaseModel):
    _id: str
    name: str
    group: str
    board: str
    project: str
    parentTask: Optional[str] = None
    types: List[str] = []
    priority: TaskPriority
    hrid: str
    followers: Dict[str, str]
    archiver: Optional[str] = None
    completed: bool
    assignees: List[str] = []
    subtasks: List[str] = []
    milestones: List[str] = []
    dueStart: Optional[str] = None
    dueEnd: Optional[str] = None
    rightConnectors: List[str] = []
    leftConnectors: List[str] = []
    archivedAt: Optional[str] = None
    completedAt: Optional[str] = None
    customFields: List[TaskCustomField] = []
    deleter: Optional[str] = None
    deletedAt: Optional[str] = None
    creator: str
    createdAt: str
    updatedAt: str
    document: str
    editor: Optional[str] = None
    milestone: Optional[str] = None


class TaskResponse(BaseModel):
    payload: Dict[str, Any]
    type: str

    @property
    def task(self) -> Task:
        return self.payload["task"]


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

    def model_dump(self, **kwargs):
        # Remove None values from the dict
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


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

    def model_dump(self, **kwargs):
        # Remove None values from the dict
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None} 