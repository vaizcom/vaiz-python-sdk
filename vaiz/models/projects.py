from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from .enums import EIcon, EColor


class Project(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    color: EColor
    slug: str
    icon: EIcon
    creator: str
    archiver: Optional[str] = None
    archived_at: Optional[str] = Field(None, alias="archivedAt")
    space: str
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)


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