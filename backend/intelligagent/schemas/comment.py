from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base Comment schema with common fields
class CommentBase(BaseModel):
    body: str
    is_internal: bool = False

# Schema for creating a new comment
class CommentCreate(CommentBase):
    ticket_id: int
    author_id: int

# Schema for comment responses (what the API returns)
class Comment(CommentBase):
    id: int
    ticket_id: int
    author_id: int
    created_at: str
    
    class Config:
        from_attributes = True

# Schema for comment with author info
class CommentWithAuthor(Comment):
    author_name: str
    author_email: str
