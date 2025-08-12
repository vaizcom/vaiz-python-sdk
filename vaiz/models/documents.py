from pydantic import BaseModel, Field, ConfigDict
from typing import List, Any, Dict


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
    files: List[str] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):  # type: ignore[override]
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class ReplaceDocumentResponse(BaseModel):
    """Response model for document replacement - returns empty object on success."""
    pass


