from sqlalchemy.orm import Session
from intelligagent.db.models import User
from intelligagent.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database."""
    db_user = User(
        email=user.email,
        name=user.name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> User:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    """Get a user by email address."""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    """Update a user's information."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user
