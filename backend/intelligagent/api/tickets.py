from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from intelligagent.db.database import get_db
from intelligagent.schemas.ticket import Ticket, TicketCreate, TicketUpdate, TicketWithRequester
from intelligagent.services import ticket_service, user_service

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=Ticket)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """Create a new ticket."""
    # Verify that the requester exists
    db_user = user_service.get_user(db, user_id=ticket.requester_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Requester not found")
    
    return ticket_service.create_ticket(db=db, ticket=ticket)

@router.get("/", response_model=List[Ticket])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of tickets."""
    tickets = ticket_service.get_tickets(db, skip=skip, limit=limit)
    return tickets

@router.get("/{ticket_id}", response_model=Ticket)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get a specific ticket by ID."""
    db_ticket = ticket_service.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    """Update a ticket."""
    db_ticket = ticket_service.update_ticket(db, ticket_id=ticket_id, ticket_update=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.get("/user/{user_id}", response_model=List[Ticket])
def read_tickets_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all tickets created by a specific user."""
    # Verify that the user exists
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    tickets = ticket_service.get_tickets_by_user(db, user_id=user_id)
    return tickets
