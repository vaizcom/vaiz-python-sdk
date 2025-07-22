from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import TaskPriority, CustomField, VaizBaseModel
from .enums import EUploadFileType, EKind


class TaskFile(VaizBaseModel):
    id: str = Field(..., alias="_id")
    url: str
    name: str
    ext: str
    type: EUploadFileType
    # Optional fields that may come from different file types
    dimension: Optional[List[int]] = None
    size: Optional[int] = None
    dominant_color: Optional[Dict[str, Any]] = None
    mime: Optional[str] = None
    original_name: Optional[str] = None
    date: Optional[datetime] = None
    owner: Optional[str] = None
    access_kind: Optional[str] = None
    access_kind_id: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class TaskCustomField(BaseModel):
    id: str
    value: Any
    _id: str


class Task(VaizBaseModel):
    id: str = Field(..., alias="_id")
    name: str
    group: str
    board: str
    project: str
    parent_task: Optional[str] = Field(default=None, alias="parentTask")
    types: List[str] = []
    priority: TaskPriority
    hrid: str
    followers: Dict[str, str]
    archiver: Optional[str] = None
    completed: bool
    assignees: List[str] = []
    subtasks: List[str] = []
    milestones: List[str] = []
    due_start: Optional[datetime] = Field(default=None, alias="dueStart")
    due_end: Optional[datetime] = Field(default=None, alias="dueEnd")
    right_connectors: List[str] = Field(default_factory=list, alias="rightConnectors")
    left_connectors: List[str] = Field(default_factory=list, alias="leftConnectors")
    archived_at: Optional[datetime] = Field(default=None, alias="archivedAt")
    completed_at: Optional[datetime] = Field(default=None, alias="completedAt")
    custom_fields: List[TaskCustomField] = Field(default_factory=list, alias="customFields")
    deleter: Optional[str] = None
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    creator: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    document: str
    editor: Optional[str] = None
    milestone: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class TaskResponse(BaseModel):
    payload: Dict[str, Any]
    type: str

    @property
    def task(self) -> Task:
        task_data = self.payload["task"]
        # Ensure the task data has the correct field mapping
        if "_id" in task_data and "id" not in task_data:
            task_data["id"] = task_data["_id"]
        return Task(**task_data)


class CreateTaskRequest(VaizBaseModel):
    name: str
    group: str
    board: str
    project: str
    description: Optional[str] = None
    parent_task: Optional[str] = Field(default=None, alias="parentTask")
    types: List[str] = []
    priority: TaskPriority = TaskPriority.General
    completed: bool = False
    assignees: List[str] = []
    subtasks: List[str] = []
    milestones: List[str] = []
    due_start: Optional[datetime] = Field(default=None, alias="dueStart")
    due_end: Optional[datetime] = Field(default=None, alias="dueEnd")
    right_connectors: List[str] = Field(default_factory=list, alias="rightConnectors")
    left_connectors: List[str] = Field(default_factory=list, alias="leftConnectors")
    custom_fields: List[CustomField] = Field(default_factory=list, alias="customFields")
    files: List[TaskFile] = []

    def model_dump(self, **kwargs):
        # Remove None values from the dict
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class EditTaskRequest(VaizBaseModel):
    task_id: str = Field(..., alias="taskId")
    name: Optional[str] = None
    parent_task: Optional[str] = Field(default=None, alias="parentTask")
    types: Optional[List[str]] = None
    priority: Optional[TaskPriority] = None
    completed: Optional[bool] = None
    assignees: Optional[List[str]] = None
    subtasks: Optional[List[str]] = None
    milestones: Optional[List[str]] = None
    due_start: Optional[datetime] = Field(default=None, alias="dueStart")
    due_end: Optional[datetime] = Field(default=None, alias="dueEnd")
    right_connectors: Optional[List[str]] = Field(default=None, alias="rightConnectors")
    left_connectors: Optional[List[str]] = Field(default=None, alias="leftConnectors")
    custom_fields: Optional[List[CustomField]] = Field(default=None, alias="customFields")
    description: Optional[str] = None
    files: Optional[List[TaskFile]] = None

    def model_dump(self, **kwargs):
        # Remove None values from the dict
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class TaskUploadFile(BaseModel):
    path: str
    type: Optional[EUploadFileType] = None

    def __init__(self, **data):
        super().__init__(**data)
        # Auto-detect type if not provided
        if self.type is None:
            self.type = self._detect_file_type(self.path)
    
    def _detect_file_type(self, file_path: str) -> EUploadFileType:
        """
        Auto-detect file type based on file extension.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            EUploadFileType: Detected file type
        """
        import os
        ext = os.path.splitext(file_path)[1].lower()
        
        # Image files
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
            return EUploadFileType.Image
        
        # Video files
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
            return EUploadFileType.Video
        
        # Document files
        elif ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
            return EUploadFileType.Pdf
        
        # Archive and audio files are not supported by EUploadFileType, so skip
        # Default to PDF for unknown extensions
        return EUploadFileType.Pdf 


class GetHistoryRequest(VaizBaseModel):
    kind: EKind
    kindId: str
    excludeKeys: Optional[List[str]] = None
    lastLoadedDate: Optional[int] = 0

class HistoryData(VaizBaseModel):
    _id: str
    hrid: Optional[str] = None
    name: Optional[str] = None
    # Additional fields may be present depending on key
    taskPriority: Optional[int] = None
    board: Optional[str] = None
    members: Optional[List[str]] = None
    project: Optional[str] = None
    dueStart: Optional[str] = None
    dueEnd: Optional[str] = None
    # Accept arbitrary extra fields
    class Config:
        extra = "allow"

class HistoryItem(VaizBaseModel):
    _id: str
    taskId: str
    creatorId: str
    createdAt: str
    data: HistoryData
    key: str
    type: int
    updatedAt: str
    boardId: Optional[str] = None

class GetHistoryPayload(VaizBaseModel):
    histories: List[HistoryItem]

class GetHistoryResponse(VaizBaseModel):
    payload: GetHistoryPayload
    type: str 