from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ProfileEmail(BaseModel):
    email: str
    confirmed: bool
    primary: bool


class ProfileColor(BaseModel):
    color: Optional[str] = None  # Hex color string
    isDark: Optional[bool] = None


class Profile(BaseModel):
    id: str = Field(..., alias="_id")
    fullName: str
    nickName: str
    email: str
    emails: List[ProfileEmail]
    color: ProfileColor = Field(default_factory=ProfileColor)
    avatarMode: int
    incompleteSteps: List[str]
    registeredDate: str
    recoveryCodes: List[str]
    passwordChangedDate: str
    passwordHash: str
    memberId: str
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    cData: Dict[str, Optional[str]]


class ProfileResponse(BaseModel):
    type: str
    payload: Dict[str, Profile] = Field(..., alias="payload")

    @property
    def profile(self) -> Profile:
        return self.payload["profile"] 