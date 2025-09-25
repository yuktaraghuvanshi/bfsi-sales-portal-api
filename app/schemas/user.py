from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from uuid import UUID
import re

# -----------------------
# Allowed values
# -----------------------
ALLOWED_ROLES = {"admin", "manager", "sales"}
ALLOWED_STATUS = {"new", "in_progress", "closed"}
ALLOWED_PRIORITY = {1, 2, 3}

# -----------------------
# User Schema
# -----------------------
class UserBase(BaseModel):
    username: constr(
        min_length=3, 
        max_length=80, 
        regex=r'^[A-Za-z0-9._-]{3,80}$'
    )
    email: Optional[EmailStr]
    full_name: Optional[str]
    phone: Optional[str]
    role: Optional[str] = "sales"

    @validator("role")
    def validate_role(cls, v: Optional[str]):
        if v and v not in ALLOWED_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(ALLOWED_ROLES)}")
        return v

# -----------------------
# Create User Schema
# -----------------------
class UserCreate(UserBase):
    password: constr(min_length=8)

    @validator("password")
    def validate_password(cls, v: str) -> str:
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain a lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        return v

    @validator("phone")
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Strict E.164 format: + followed by 8–15 digits"""
        if v is None:
            return v
        pattern = re.compile(r"^\+\d{8,15}$")
        if not pattern.match(v):
            raise ValueError("Phone must be in E.164 format (e.g. +61412345678)")
        return v

    @validator("email")
    def validate_email_required(cls, v: Optional[str], values) -> Optional[str]:
        if values.get("role") == "user" and not v:
            raise ValueError("Email is required for users")
        return v

# -----------------------
# Lead / Task Schema
# -----------------------
class LeadBase(BaseModel):
    status: Optional[str] = "new"
    priority: Optional[int] = 1

    @validator("status")
    def validate_status(cls, v: Optional[str]):
        if v and v not in ALLOWED_STATUS:
            raise ValueError(f"Status must be one of: {', '.join(ALLOWED_STATUS)}")
        return v

    @validator("priority")
    def validate_priority(cls, v: Optional[int]):
        if v and v not in ALLOWED_PRIORITY:
            raise ValueError(f"Priority must be one of: {', '.join(map(str, ALLOWED_PRIORITY))}")
        return v

# -----------------------
# Output Schemas
# -----------------------
class UserOut(UserBase):
    user_id: UUID
    is_active: bool

    class Config:
        orm_mode = True

class RefreshRequest(BaseModel):
    refresh_token: str
