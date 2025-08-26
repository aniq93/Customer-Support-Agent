from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from intelligagent.db.database import Base
import enum

class UserRole(str, enum.Enum):
    """User roles in the system."""
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"

class TicketStatus(str, enum.Enum):
    """Ticket status values."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketPriority(str, enum.Enum):
    """Ticket priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class User(Base):
    """User model representing system users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tickets_created = relationship("Ticket", foreign_keys="Ticket.requester_id", back_populates="requester")
    tickets_assigned = relationship("Ticket", foreign_keys="Ticket.assignee_id", back_populates="assignee")
    comments = relationship("Comment", back_populates="author")

class Ticket(Base):
    """Ticket model representing customer support requests."""
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="tickets_created")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="tickets_assigned")
    comments = relationship("Comment", back_populates="ticket")

class Comment(Base):
    """Comment model representing conversation on tickets."""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False, nullable=False)  # Internal notes vs customer-visible
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("User", back_populates="comments")
