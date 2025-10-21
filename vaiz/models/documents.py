from pydantic import BaseModel, Field, ConfigDict
from typing import List, Any, Dict, Optional
from datetime import datetime
from .base import VaizBaseModel
from .enums import Kind


class GetDocumentRequest(BaseModel):
    """Request model for fetching a JSON document by its ID."""
    document_id: str = Field(..., alias="documentId")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):  # type: ignore[override]
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class ReplaceDocumentRequest(BaseModel):
    """Request model for replacing document content."""
    document_id: str = Field(..., alias="documentId")
    description: str

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):  # type: ignore[override]
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class ReplaceDocumentResponse(BaseModel):
    """Response model for document replacement - returns empty object on success."""
    pass


class Document(VaizBaseModel):
    """Model representing a Vaiz document."""
    id: str = Field(..., alias="_id")
    title: str
    size: int
    contributor_ids: List[str] = Field(default_factory=list, alias="contributorIds")
    archiver: Optional[str] = None
    followers: Dict[str, str] = Field(default_factory=dict)
    archived_at: Optional[datetime] = Field(default=None, alias="archivedAt")
    kind_id: str = Field(..., alias="kindId")
    kind: Kind
    creator: str
    map: List[Any] = Field(default_factory=list)
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    bucket: str

    model_config = ConfigDict(populate_by_name=True)


class GetDocumentsRequest(VaizBaseModel):
    """Request model for getting documents list."""
    kind: Kind
    kind_id: str = Field(..., alias="kindId")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class GetDocumentsPayload(VaizBaseModel):
    """Payload containing the list of documents."""
    documents: List[Document]


class GetDocumentsResponse(VaizBaseModel):
    """Response model for getting documents list."""
    payload: GetDocumentsPayload
    type: str


