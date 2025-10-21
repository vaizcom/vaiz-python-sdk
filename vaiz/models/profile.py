from pydantic import BaseModel, Field
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
    """Represents the user profile."""
    id: str = Field(..., alias="_id")
    full_name: Optional[str] = Field(None, alias="fullName")
    nick_name: Optional[str] = Field(None, alias="nickName")
    email: str
    emails: Optional[List[ProfileEmail]] = []
    color: ProfileColor = Field(default_factory=ProfileColor)
    avatar_mode: AvatarMode = Field(..., alias="avatarMode")
    incomplete_steps: Optional[List[str]] = Field(default_factory=list, alias="incompleteSteps")
    registered_date: datetime = Field(..., alias="registeredDate")
    recovery_codes: Optional[List[Dict[str, str]]] = Field(default_factory=list, alias="recoveryCodes")
    password_changed_date: Optional[datetime] = Field(None, alias="passwordChangedDate")
    member_id: Optional[str] = Field(None, alias="memberId")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    c_data: Optional[Dict[str, Optional[str]]] = Field(default_factory=dict, alias="cData")
    is_email_confirmed: Optional[bool] = Field(None, alias="isEmailConfirmed")
    avatar: Optional[str] = None
    invited: Optional[bool] = None
    recovery_codes_viewed_date: Optional[datetime] = Field(None, alias="recoveryCodesViewedDate")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    webauthn_credentials: Optional[List[Dict[str, Any]]] = Field(default_factory=list, alias="webAuthnCredentials")


class ProfileResponse(BaseModel):
    type: str
    payload: Dict[str, Profile]

    @property
    def profile(self) -> Profile:
        return self.payload["profile"] 