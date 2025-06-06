from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


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
    priority: int
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