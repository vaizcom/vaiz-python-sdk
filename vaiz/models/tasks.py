from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from datetime import datetime
from .base import TaskPriority, CustomField, VaizBaseModel
from .documents import ReplaceDocumentResponse
from .enums import UploadFileType, Kind

if TYPE_CHECKING:
    # Avoid runtime import cycle; type-checking only
    from vaiz.client import VaizClient

class TaskFile(VaizBaseModel):
    id: str = Field(..., alias="_id")
    url: str
    name: str
    ext: str
    type: UploadFileType
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
    blocking: List[str] = Field(default_factory=list, alias="rightConnectors", serialization_alias="rightConnectors")
    blockers: List[str] = Field(default_factory=list, alias="leftConnectors", serialization_alias="leftConnectors")
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

    def get_task_description(self, client: 'VaizClient') -> Dict[str, Any]:
        """Convenience method to fetch this task's description document body.

        Args:
            client (VaizClient): An initialized Vaiz client instance

        Returns:
            Dict[str, Any]: Parsed JSON document body for this task's description
        """
        return client.get_json_document(self.document)

    def update_task_description(
        self,
        client: 'VaizClient',
        description: str,
    ) -> ReplaceDocumentResponse:
        """Replace this task's description content.

        Uses the document API to completely replace the description content for
        the document associated with this task.

        Args:
            client (VaizClient): An initialized Vaiz client instance
            description (str): New description content as plain text

        Returns:
            ReplaceDocumentResponse: Response object from the replace operation
        """
        return client.replace_document(self.document, description)


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
    board: str
    group: Optional[str] = None
    project: Optional[str] = None
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
    blocking: List[str] = Field(default_factory=list, alias="rightConnectors", serialization_alias="rightConnectors")
    blockers: List[str] = Field(default_factory=list, alias="leftConnectors", serialization_alias="leftConnectors")
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
    blocking: Optional[List[str]] = Field(default=None, alias="rightConnectors", serialization_alias="rightConnectors")
    blockers: Optional[List[str]] = Field(default=None, alias="leftConnectors", serialization_alias="leftConnectors")
    custom_fields: Optional[List[CustomField]] = Field(default=None, alias="customFields")
    description: Optional[str] = None
    files: Optional[List[TaskFile]] = None

    def model_dump(self, **kwargs):
        # Remove None values from the dict
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class TaskUploadFile(BaseModel):
    path: str
    type: Optional[UploadFileType] = None

    def __init__(self, **data):
        super().__init__(**data)
        # Auto-detect type if not provided
        if self.type is None:
            self.type = self._detect_file_type(self.path)
    
    def _detect_file_type(self, file_path: str) -> UploadFileType:
        """
        Auto-detect file type based on file extension.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            UploadFileType: Detected file type
        """
        import os
        ext = os.path.splitext(file_path)[1].lower()
        
        # Image files
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
            return UploadFileType.Image
        
        # Video files
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
            return UploadFileType.Video
        
        # Document files
        elif ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
            return UploadFileType.Pdf
        
        # Archive and audio files are not supported by UploadFileType, so skip
        # Default to PDF for unknown extensions
        return UploadFileType.Pdf 


class GetHistoryRequest(VaizBaseModel):
    kind: Kind
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
    
    model_config = ConfigDict(extra="allow")  # Accept arbitrary extra fields

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


class GetTasksRequest(VaizBaseModel):
    ids: Optional[List[str]] = None
    limit: Optional[int] = Field(default=50, ge=1, le=50)  # Maximum 50 tasks per page
    skip: Optional[int] = Field(default=0, ge=0)
    board: Optional[str] = None
    project: Optional[str] = None
    assignees: Optional[List[str]] = None
    parent_task: Optional[str] = Field(default=None, alias="parentTask")
    milestones: Optional[List[str]] = None
    completed: Optional[bool] = None
    archived: Optional[bool] = None

    def model_dump(self, **kwargs):
        # Remove None values from the dict
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class GetTasksPayload(VaizBaseModel):
    tasks: List[Task]


class GetTasksResponse(VaizBaseModel):
    payload: GetTasksPayload
    type: str 