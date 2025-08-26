"""
Tests for the user service layer.
"""
import pytest
from sqlalchemy.orm import Session

from intelligagent.services.user_service import (
    create_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user
)
from intelligagent.schemas.user import UserCreate, UserUpdate
from intelligagent.db.models import User, UserRole


class TestUserService:
    """Test cases for user service functions."""
    
    def test_create_user_success(self, db_session):
        """Test successful user creation."""
        # Arrange
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            role=UserRole.CUSTOMER
        )
        
        # Act
        created_user = create_user(db_session, user_data)
        
        # Assert
        assert created_user is not None
        assert created_user.email == "test@example.com"
        assert created_user.name == "Test User"
        assert created_user.role == UserRole.CUSTOMER
        assert created_user.id is not None
        assert created_user.created_at is not None
    
    def test_get_user_by_id_success(self, db_session, db_user):
        """Test getting user by ID when user exists."""
        # Act
        retrieved_user = get_user(db_session, db_user.id)
        
        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == db_user.id
        assert retrieved_user.email == db_user.email
    
    def test_get_user_by_id_not_found(self, db_session):
        """Test getting user by ID when user doesn't exist."""
        # Act
        retrieved_user = get_user(db_session, 999)
        
        # Assert
        assert retrieved_user is None
    
    def test_get_user_by_email_success(self, db_session, db_user):
        """Test getting user by email when user exists."""
        # Act
        retrieved_user = get_user_by_email(db_session, db_user.email)
        
        # Assert
        assert retrieved_user is not None
        assert retrieved_user.email == db_user.email
    
    def test_get_user_by_email_not_found(self, db_session):
        """Test getting user by email when user doesn't exist."""
        # Act
        retrieved_user = get_user_by_email(db_session, "nonexistent@example.com")
        
        # Assert
        assert retrieved_user is None
    
    def test_get_users_with_pagination(self, db_session):
        """Test getting users with pagination."""
        # Arrange - Create multiple users
        users_data = [
            UserCreate(email=f"user{i}@example.com", name=f"User {i}", role=UserRole.CUSTOMER)
            for i in range(5)
        ]
        
        for user_data in users_data:
            create_user(db_session, user_data)
        
        # Act
        users = get_users(db_session, skip=0, limit=3)
        
        # Assert
        assert len(users) == 3
        
        # Act - Test offset
        users_offset = get_users(db_session, skip=2, limit=3)
        assert len(users_offset) == 3
    
    def test_update_user_success(self, db_session, db_user):
        """Test successful user update."""
        # Arrange
        update_data = UserUpdate(name="Updated Name", role=UserRole.AGENT)
        
        # Act
        updated_user = update_user(db_session, db_user.id, update_data)
        
        # Assert
        assert updated_user is not None
        assert updated_user.name == "Updated Name"
        assert updated_user.role == UserRole.AGENT
        assert updated_user.email == db_user.email  # Should remain unchanged
    
    def test_update_user_not_found(self, db_session):
        """Test updating user that doesn't exist."""
        # Arrange
        update_data = UserUpdate(name="Updated Name")
        
        # Act
        updated_user = update_user(db_session, 999, update_data)
        
        # Assert
        assert updated_user is None
