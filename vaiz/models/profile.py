from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import VaizBaseModel


class ProfileEmail(BaseModel):
    email: str
    confirmed: bool
    primary: bool


class ProfileColor(BaseModel):
    color: Optional[str] = None  # Hex color string
    isDark: Optional[bool] = None


class Profile(VaizBaseModel):
    """Represents the user profile."""
    id: str = Field(..., alias="_id")
    fullName: Optional[str] = None
    nickName: Optional[str] = None  
    email: str
    emails: Optional[List[ProfileEmail]] = []
    color: ProfileColor = Field(default_factory=ProfileColor)
    avatarMode: int  # This comes as integer from API
    incompleteSteps: Optional[List[str]] = []
    registeredDate: datetime
    recoveryCodes: Optional[List[Dict[str, str]]] = []
    passwordChangedDate: datetime
    passwordHash: Optional[str] = None
    memberId: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    cData: Optional[Dict[str, Optional[str]]] = {}


class ProfileResponse(BaseModel):
    type: str
    payload: Dict[str, Profile] = Field(..., alias="payload")

    @property
    def profile(self) -> Profile:
        return self.payload["profile"] 