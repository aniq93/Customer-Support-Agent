from pydantic import BaseModel, EmailStr
from typing import Optional
from intelligagent.db.models import UserRole
from datetime import datetime

# Base User schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.CUSTOMER

# Schema for creating a new user
class UserCreate(UserBase):
    pass

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None

# Schema for user responses (what the API returns)
class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models
