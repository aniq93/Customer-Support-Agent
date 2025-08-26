from sqlalchemy.orm import Session
from intelligagent.db.models import Ticket, User
from intelligagent.schemas.ticket import TicketCreate, TicketUpdate

def create_ticket(db: Session, ticket: TicketCreate) -> Ticket:
    """Create a new ticket in the database."""
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        requester_id=ticket.requester_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int) -> Ticket:
    """Get a ticket by ID."""
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of tickets with pagination."""
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_tickets_by_user(db: Session, user_id: int):
    """Get all tickets created by a specific user."""
    return db.query(Ticket).filter(Ticket.requester_id == user_id).all()

def get_tickets_by_assignee(db: Session, assignee_id: int):
    """Get all tickets assigned to a specific user."""
    return db.query(Ticket).filter(Ticket.assignee_id == assignee_id).all()

def update_ticket(db: Session, ticket_id: int, ticket_update: TicketUpdate) -> Ticket:
    """Update a ticket's information."""
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None
    
    update_data = ticket_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ticket, field, value)
    
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket_with_requester(db: Session, ticket_id: int):
    """Get a ticket with requester information."""
    return db.query(Ticket, User).join(User, Ticket.requester_id == User.id).filter(Ticket.id == ticket_id).first()
