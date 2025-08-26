from pydantic import BaseModel
from typing import Optional, List
from intelligagent.db.models import TicketStatus, TicketPriority

# Base Ticket schema with common fields
class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.MEDIUM

# Schema for creating a new ticket
class TicketCreate(TicketBase):
    requester_id: int

# Schema for updating a ticket
class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assignee_id: Optional[int] = None

# Schema for ticket responses (what the API returns)
class Ticket(TicketBase):
    id: int
    status: TicketStatus
    requester_id: int
    assignee_id: Optional[int] = None
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

# Schema for ticket with requester info
class TicketWithRequester(Ticket):
    requester_name: str
    requester_email: str
