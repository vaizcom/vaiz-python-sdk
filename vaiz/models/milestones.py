from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, TYPE_CHECKING, Any, Union
from datetime import datetime
from .base import VaizBaseModel
from .enums import Color

if TYPE_CHECKING:
    from .tasks import Task


class CreateMilestoneRequest(VaizBaseModel):
    """Request model for creating a milestone."""
    name: str
    description: Optional[str] = None
    board: str
    project: str
    due_start: Optional[datetime] = Field(default=None, alias="dueStart")
    due_end: Optional[datetime] = Field(default=None, alias="dueEnd")
    tags: List[str] = []
    color: Union[str, Color] = Color.Blue  # Default blue color


class Milestone(VaizBaseModel):
    """Represents a milestone in the system."""
    id: str = Field(..., alias="_id")
    name: str
    description: Optional[str] = None
    board: str
    project: str
    creator: str
    archiver: Optional[str] = None
    due_start: Optional[datetime] = Field(default=None, alias="dueStart")
    due_end: Optional[datetime] = Field(default=None, alias="dueEnd")
    tags: List[str] = []
    archived_at: Optional[datetime] = Field(default=None, alias="archivedAt")
    is_archived: bool = Field(False, alias="isArchived")
    is_active: bool = Field(True, alias="isActive")
    is_completed: bool = Field(False, alias="isCompleted")
    color: Optional[Union[str, Color]] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    deleter: Optional[str] = None
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    followers: Optional[Dict[str, str]] = {}
    document: Optional[str] = None
    total: Optional[int] = 0
    completed: Optional[int] = 0
    editor: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class MilestonesPayload(BaseModel):
    milestones: List[Milestone]


class MilestonesResponse(BaseModel):
    type: str
    payload: MilestonesPayload

    @property
    def milestones(self) -> List[Milestone]:
        return self.payload.milestones


class CreateMilestonePayload(BaseModel):
    milestone: Milestone


class CreateMilestoneResponse(BaseModel):
    type: str
    payload: CreateMilestonePayload

    @property
    def milestone(self) -> Milestone:
        return self.payload.milestone


class GetMilestonePayload(BaseModel):
    milestone: Milestone


class GetMilestoneResponse(BaseModel):
    type: str
    payload: GetMilestonePayload

    @property
    def milestone(self) -> Milestone:
        return self.payload.milestone


class EditMilestoneRequest(VaizBaseModel):
    """Request model for editing a milestone."""
    milestone_id: str = Field(..., alias="_id")  # Use alias to send as "_id" to API
    name: Optional[str] = None
    description: Optional[str] = None
    due_start: Optional[datetime] = Field(default=None, alias="dueStart")
    due_end: Optional[datetime] = Field(default=None, alias="dueEnd")
    tags: Optional[List[str]] = None
    color: Optional[Union[str, Color]] = None

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        # Remove None values from the dict and use alias by default
        kwargs.setdefault('by_alias', True)
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


class EditMilestonePayload(BaseModel):
    milestone: Milestone


class EditMilestoneResponse(BaseModel):
    type: str
    payload: EditMilestonePayload

    @property
    def milestone(self) -> Milestone:
        return self.payload.milestone


class ToggleMilestoneRequest(BaseModel):
    task_id: str = Field(..., alias="taskId")
    milestone_ids: List[str] = Field(..., alias="milestoneIds")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        return super().model_dump(by_alias=True, **kwargs)


class ToggleMilestonePayload(BaseModel):
    task: Dict[str, Any]  # Using Dict to avoid circular import issues


class ToggleMilestoneResponse(BaseModel):
    type: str
    payload: ToggleMilestonePayload

    @property
    def task(self) -> "Task":
        # Import here to avoid circular import
        from .tasks import Task
        task_data = self.payload.task
        # Ensure the task data has the correct field mapping
        if "_id" in task_data and "id" not in task_data:
            task_data["id"] = task_data["_id"]
        return Task(**task_data) 