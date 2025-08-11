from pydantic import BaseModel, Field, ConfigDict


class GetDocumentRequest(BaseModel):
    """Request model for fetching a JSON document by its ID."""
    document_id: str = Field(..., alias="documentId")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):  # type: ignore[override]
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


