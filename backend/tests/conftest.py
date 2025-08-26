import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

from intelligagent.db.database import Base, get_db
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from intelligagent.db.models import User, Ticket, Comment, UserRole, TicketStatus, TicketPriority
from intelligagent.schemas.user import UserCreate
from intelligagent.schemas.ticket import TicketCreate

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override the database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db_engine():
    """Create database engine for testing."""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    """Create a new database session for a test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Create a test client with overridden database session."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# Test data factories
@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "role": UserRole.CUSTOMER
    }

@pytest.fixture
def sample_ticket_data():
    """Sample ticket data for testing."""
    return {
        "title": "Test Ticket",
        "description": "This is a test ticket",
        "priority": TicketPriority.MEDIUM,
        "requester_id": 1
    }

@pytest.fixture
def sample_comment_data():
    """Sample comment data for testing."""
    return {
        "body": "This is a test comment",
        "is_internal": False,
        "ticket_id": 1,
        "author_id": 1
    }

@pytest.fixture
def db_user(db_session, sample_user_data):
    """Create a test user in the database."""
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def db_ticket(db_session, db_user, sample_ticket_data):
    """Create a test ticket in the database."""
    ticket_data = sample_ticket_data.copy()
    ticket_data["requester_id"] = db_user.id
    ticket = Ticket(**ticket_data)
    db_session.add(ticket)
    db_session.commit()
    db_session.refresh(ticket)
    return ticket

@pytest.fixture
def db_comment(db_session, db_ticket, db_user, sample_comment_data):
    """Create a test comment in the database."""
    comment_data = sample_comment_data.copy()
    comment_data["ticket_id"] = db_ticket.id
    comment_data["author_id"] = db_user.id
    comment = Comment(**comment_data)
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment

@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing."""
    user = User(
        email="admin@example.com",
        name="Admin User",
        role=UserRole.ADMIN
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def agent_user(db_session):
    """Create an agent user for testing."""
    user = User(
        email="agent@example.com",
        name="Agent User",
        role=UserRole.AGENT
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
