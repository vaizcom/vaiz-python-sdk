from pydantic import BaseModel
from typing import List, Optional
from .base import TaskPriority, CustomField


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