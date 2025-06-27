from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from vaiz.models.enums import EUploadFileType

class UploadedFile(BaseModel):
    dominant_color: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="dominantColor")
    dimension: Optional[list] = Field(default_factory=list)
    id: str = Field(..., alias="_id")
    date: str
    owner: str
    url: str
    ext: str
    name: str
    original_name: str = Field(..., alias="originalName")
    mime: str
    size: int
    type: EUploadFileType
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