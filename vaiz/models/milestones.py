from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict


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

    model_config = ConfigDict(populate_by_name=True)


class MilestonesPayload(BaseModel):
    milestones: List[Milestone]


class MilestonesResponse(BaseModel):
    type: str
    payload: MilestonesPayload

    @property
    def milestones(self) -> List[Milestone]:
        return self.payload.milestones 