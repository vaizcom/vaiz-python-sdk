from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import VaizBaseModel
from .enums import AvatarMode


class ProfileEmail(BaseModel):
    email: str
    confirmed: bool
    primary: bool


class ProfileColor(BaseModel):
    color: Optional[str] = None  # Color name
    is_dark: Optional[bool] = Field(None, alias="isDark")


class Profile(VaizBaseModel):
    """
    Represents the current member's profile in the current space.

    The profile is per-space: name, avatar, color and email belong to the member,
    so `id` is the member ID and `user_id` is the ID of the underlying user account.
    """
    id: str = Field(..., alias="_id")
    member_id: Optional[str] = Field(None, alias="memberId")
    user_id: Optional[str] = Field(None, alias="user")
    space: Optional[str] = None
    status: Optional[str] = None
    full_name: Optional[str] = Field(None, alias="fullName")
    nick_name: Optional[str] = Field(None, alias="nickName")
    email: str
    color: ProfileColor = Field(default_factory=ProfileColor)
    avatar_mode: AvatarMode = Field(..., alias="avatarMode")
    avatar: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    joined_date: Optional[datetime] = Field(None, alias="joinedDate")
    invited_by: Optional[str] = Field(None, alias="invitedBy")
    kind: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    # User account fields returned only by API versions before Release 100.
    emails: Optional[List[ProfileEmail]] = Field(default_factory=list)
    incomplete_steps: Optional[List[str]] = Field(default_factory=list, alias="incompleteSteps")
    registered_date: Optional[datetime] = Field(None, alias="registeredDate")
    recovery_codes: Optional[List[Dict[str, str]]] = Field(default_factory=list, alias="recoveryCodes")
    password_changed_date: Optional[datetime] = Field(None, alias="passwordChangedDate")
    c_data: Optional[Dict[str, Optional[str]]] = Field(default_factory=dict, alias="cData")
    is_email_confirmed: Optional[bool] = Field(None, alias="isEmailConfirmed")
    invited: Optional[bool] = None
    recovery_codes_viewed_date: Optional[datetime] = Field(None, alias="recoveryCodesViewedDate")
    webauthn_credentials: Optional[List[Dict[str, Any]]] = Field(default_factory=list, alias="webAuthnCredentials")

    @model_validator(mode="after")
    def _resolve_ids(self) -> "Profile":
        # Before Release 100 `_id` was the user ID and the member ID came in `memberId`.
        if self.member_id is None:
            self.__dict__["member_id"] = self.id
        elif self.user_id is None:
            self.__dict__["user_id"] = self.id
        return self


class ProfileResponse(BaseModel):
    type: str
    payload: Dict[str, Profile]

    @property
    def profile(self) -> Profile:
        return self.payload["profile"]


class EditProfileRequest(BaseModel):
    """
    Request model for editing the current member's profile in the current space.

    Only provided fields are updated. Changing `full_name` or `nick_name` regenerates
    the avatar if the member uses a generated avatar.
    """
    full_name: Optional[str] = Field(None, alias="fullName")
    nick_name: Optional[str] = Field(None, alias="nickName")
    position: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")

    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kwargs):  # type: ignore[override]
        data = super().model_dump(by_alias=True, **kwargs)
        return {k: v for k, v in data.items() if v is not None}
