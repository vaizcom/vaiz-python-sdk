from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import TaskPriority, CustomField
from .enums import EUploadFileType


class TaskFile(BaseModel):
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
    date: Optional[str] = None
    owner: Optional[str] = None
    access_kind: Optional[str] = None
    access_kind_id: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class TaskCustomField(BaseModel):
    id: str
    value: Any
    _id: str


class Task(BaseModel):
    id: str = Field(..., alias="_id")
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
    description: Optional[str] = None
    files: List[TaskFile] = []

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
        
        # Audio files
        elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg']:
            return EUploadFileType.Audio
        
        # Document files
        elif ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
            return EUploadFileType.Pdf
        
        # Archive files
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return EUploadFileType.Archive
        
        # Default to PDF for unknown extensions
        return EUploadFileType.Pdf 