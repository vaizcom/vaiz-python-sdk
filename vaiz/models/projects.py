from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from .base import VaizBaseModel
from .enums import EIcon, EColor


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
    color: Optional[Union[str, EColor]] = None  # Allow both hex codes and enum values
    slug: Optional[str] = None
    icon: Optional[EIcon] = None
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