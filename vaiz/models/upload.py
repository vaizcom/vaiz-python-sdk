from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from vaiz.models.enums import UploadFileType
from .base import VaizBaseModel

class UploadedFile(VaizBaseModel):
    dominant_color: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="dominantColor")
    dimension: Optional[list] = Field(default_factory=list)
    id: str = Field(..., alias="_id")
    date: datetime
    owner: str
    url: str
    name: str
    type: UploadFileType
    ext: str
    size: int
    mime: Optional[str] = Field(default=None, alias="mime")
    original_name: str = Field(..., alias="originalName")
    access_kind: str = Field(..., alias="accessKind")
    access_kind_id: str = Field(..., alias="accessKindId")

class UploadFilePayload(BaseModel):
    file: UploadedFile

class UploadFileResponse(BaseModel):
    type: str
    payload: UploadFilePayload

    @property
    def file(self) -> UploadedFile:
        return self.payload.file 