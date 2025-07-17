from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class CommentReaction(BaseModel):
    """Model for comment reaction."""
    user_id: str
    emoji: str
    created_at: str


class Comment(BaseModel):
    """Model for comment."""
    id: str = Field(..., alias="_id")
    author_id: str = Field(..., alias="authorId")
    document_id: str = Field(..., alias="documentId")
    content: str
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    files: List[str] = []
    reactions: List[CommentReaction] = []
    has_removed_files: bool = Field(False, alias="hasRemovedFiles")
    reply_to: Optional[str] = Field(None, alias="replyTo")

    model_config = ConfigDict(populate_by_name=True)


class PostCommentRequest(BaseModel):
    """Request model for creating a comment."""
    content: str
    file_ids: List[str] = Field(default_factory=list, alias="fileIds")
    document_id: str = Field(..., alias="documentId")
    reply_to: Optional[str] = Field(None, alias="replyTo")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        """Custom serialization for correct API request."""
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class PostCommentResponse(BaseModel):
    """Response model for creating a comment."""
    payload: Dict[str, Comment]
    type: str

    @property
    def comment(self) -> Comment:
        """Get the created comment."""
        return self.payload["comment"] 