from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .base import VaizBaseModel, ColorInfo
from .enums import AvatarMode


class Member(VaizBaseModel):
    """Represents a member in the space."""
    id: str = Field(..., alias="_id")
    nick_name: Optional[str] = Field(None, alias="nickName")
    full_name: Optional[str] = Field(None, alias="fullName")
    email: str
    avatar: Optional[str] = None
    avatar_mode: AvatarMode = Field(..., alias="avatarMode")
    color: ColorInfo
    space: str
    status: str
    joined_date: str = Field(..., alias="joinedDate")  # String date from API
    updated_at: str = Field(..., alias="updatedAt")    # String date from API


class GetSpaceMembersPayload(BaseModel):
    """Payload containing list of space members."""
    members: List[Member]


class GetSpaceMembersResponse(BaseModel):
    """Response model for getting space members."""
    type: str
    payload: GetSpaceMembersPayload

    @property
    def members(self) -> List[Member]:
        """Convenience property to access members directly."""
        return self.payload.members

