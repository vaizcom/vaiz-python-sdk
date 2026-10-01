from pydantic import BaseModel, ConfigDict, Field
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
    position: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    invited_by: Optional[str] = Field(None, alias="invitedBy")
    space: Optional[str] = None  # Absent for global bot members (AI, GitHub, Cursor, etc.)
    status: str
    joined_date: str = Field(..., alias="joinedDate")  # String date from API
    updated_at: str = Field(..., alias="updatedAt")    # String date from API
    kind: Optional[str] = None  # Bot kind, e.g. "AiBot", "GitHubBot"; None for regular members


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


class GetMembersRequest(BaseModel):
    """Request model for getting members by their IDs."""
    member_ids: List[str] = Field(..., alias="memberIds")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):  # type: ignore[override]
        return super().model_dump(by_alias=True, **kwargs)


class GetMembersPayload(BaseModel):
    """Payload containing the requested members."""
    members: List[Member]


class GetMembersResponse(BaseModel):
    """Response model for getting members by their IDs."""
    type: str
    payload: GetMembersPayload

    @property
    def members(self) -> List[Member]:
        """Convenience property to access members directly."""
        return self.payload.members

