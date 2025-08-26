from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from intelligagent.db.database import get_db
from intelligagent.schemas.user import User, UserCreate, UserUpdate
from intelligagent.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if user with this email already exists
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of users."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user."""
    db_user = user_service.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
