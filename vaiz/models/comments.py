from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict
from .upload import UploadedFile
from .base import VaizBaseModel


class CommentReaction(BaseModel):
    """Model for comment reaction."""

    reaction_db_id: str = Field(..., alias="_id")
    native: Optional[str] = None  # Made optional as API doesn't always return it
    emoji_id: str = Field(..., alias="id")
    member_ids: List[str] = Field(..., alias="memberIds")

    model_config = ConfigDict(populate_by_name=True)


class Comment(VaizBaseModel):
    """Represents a comment in the system."""

    id: str = Field(..., alias="_id")
    document_id: str = Field(..., alias="documentId")
    author_id: str = Field(..., alias="authorId")
    content: str
    files: List[UploadedFile] = []
    reactions: List["CommentReaction"] = []
    reply_to: Optional[str] = Field(default=None, alias="replyTo")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    edited_at: Optional[datetime] = Field(default=None, alias="editedAt")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    has_removed_files: bool = Field(False, alias="hasRemovedFiles")

    model_config = ConfigDict(populate_by_name=True)


class PostCommentRequest(BaseModel):
    """Request model for creating a comment."""

    content: str
    file_ids: List[str] = Field(default_factory=list, alias="fileIds")
    document_id: str = Field(..., alias="documentId")
    reply_to: Optional[str] = Field(default=None, alias="replyTo")

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


class ReactToCommentRequest(BaseModel):
    """Request model for reacting to a comment."""

    comment_id: str = Field(..., alias="commentId")
    id: str  # Emoji ID like "kissing_smiling_eyes"
    name: str  # Human readable name like "Kissing Face with Smiling Eyes"
    native: str  # Emoji character like "😙"
    unified: str  # Unicode codepoint like "1f619"
    keywords: List[str] = []  # Keywords for the emoji
    shortcodes: str  # Shortcode like ":kissing_smiling_eyes:"

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        """Custom serialization for correct API request."""
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class ReactToCommentResponse(BaseModel):
    """Response model for reacting to a comment."""

    payload: Dict[str, List[CommentReaction]]
    type: str

    @property
    def reactions(self) -> List[CommentReaction]:
        """Get the list of reactions."""
        return self.payload["reactions"]


class GetCommentsRequest(BaseModel):
    """Request model for getting comments."""

    document_id: str = Field(..., alias="documentId")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        """Custom serialization for correct API request."""
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class GetCommentsResponse(BaseModel):
    """Response model for getting comments."""

    payload: Dict[str, List[Comment]]
    type: str

    @property
    def comments(self) -> List[Comment]:
        """Get the list of comments."""
        return self.payload["comments"]


class EditCommentRequest(BaseModel):
    """Request model for editing a comment."""

    content: str
    comment_id: str = Field(..., alias="commentId")
    add_file_ids: List[str] = Field(default_factory=list, alias="addFileIds")
    order_file_ids: List[str] = Field(default_factory=list, alias="orderFileIds")
    remove_file_ids: List[str] = Field(default_factory=list, alias="removeFileIds")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        """Custom serialization for correct API request."""
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class EditCommentResponse(BaseModel):
    """Response model for editing a comment."""

    payload: Dict[str, Comment]
    type: str

    @property
    def comment(self) -> Comment:
        """Get the edited comment."""
        return self.payload["comment"]


class DeleteCommentRequest(BaseModel):
    """Request model for deleting a comment."""

    comment_id: str = Field(..., alias="commentId")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):
        """Custom serialization for correct API request."""
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class DeleteCommentResponse(BaseModel):
    """Response model for deleting a comment."""

    payload: Dict[str, Comment]
    type: str

    @property
    def comment(self) -> Comment:
        """Get the deleted comment."""
        return self.payload["comment"]
