from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .tasks import Task


class CreateMilestoneRequest(BaseModel):
    name: str
    board: str
    project: str

    model_config = ConfigDict(populate_by_name=True)


class Milestone(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    description: str
    due_start: Optional[str] = Field(None, alias="dueStart")
    due_end: Optional[str] = Field(None, alias="dueEnd")
    archiver: Optional[str] = None
    archived_at: Optional[str] = Field(None, alias="archivedAt")
    project: str
    followers: Dict[str, str]
    board: str
    document: str
    total: int
    completed: int
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    deleter: Optional[str] = None
    deleted_at: Optional[str] = Field(None, alias="deletedAt")
    creator: str
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


class EditMilestoneRequest(BaseModel):
    id: str = Field(..., alias="_id")
    name: Optional[str] = None
    description: Optional[str] = None
    due_start: Optional[str] = Field(None, alias="dueStart")
    due_end: Optional[str] = Field(None, alias="dueEnd")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        # Remove None values from the dict and use alias
        data = super().model_dump(by_alias=True, **kwargs)
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