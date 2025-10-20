from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime
from .base import VaizBaseModel
from .enums import Icon, Color


class Project(VaizBaseModel):
    """Represents a project in the system."""
    id: str = Field(..., alias="_id")
    name: str
    description: Optional[str] = None
    creator: str
    archived_at: Optional[datetime] = Field(default=None, alias="archivedAt")
    archiver: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    team: List[str] = []
    color: Optional[Union[str, Color]] = None  # Color enum value or string
    slug: Optional[str] = None
    icon: Optional[Icon] = None
    space: Optional[str] = None


class ProjectsPayload(BaseModel):
    projects: List[Project]


class ProjectsResponse(BaseModel):
    type: str
    payload: ProjectsPayload

    @property
    def projects(self) -> List[Project]:
        return self.payload.projects


class ProjectPayload(BaseModel):
    project: Project


class ProjectResponse(BaseModel):
    type: str
    payload: ProjectPayload

    @property
    def project(self) -> Project:
        return self.payload.project 