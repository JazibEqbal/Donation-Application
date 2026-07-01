from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    DONOR = "DONOR"
    NGO = "NGO"
    VOLUNTEER = "VOLUNTEER"
    ADMIN = "ADMIN"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole