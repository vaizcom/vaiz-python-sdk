from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any
from datetime import datetime
from .base import VaizBaseModel, ColorInfo
from .enums import AvatarMode


class Space(VaizBaseModel):
    """Represents a space in the system."""
    id: str = Field(..., alias="_id")
    name: str
    color: ColorInfo
    avatar_mode: AvatarMode = Field(..., alias="avatarMode")
    avatar: Optional[str] = None
    creator: Union[str, Dict[str, Any]]  # Can be string ID or user object
    plan: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    is_foreign: bool = Field(..., alias="isForeign")


class GetSpaceRequest(BaseModel):
    """Request model for getting space information."""
    space_id: str = Field(..., alias="spaceId")


class GetSpacePayload(BaseModel):
    """Payload containing space information."""
    space: Space


class GetSpaceResponse(BaseModel):
    """Response model for getting space information."""
    type: str
    payload: GetSpacePayload

    @property
    def space(self) -> Space:
        """Convenience property to access the space directly."""
        return self.payload.space

