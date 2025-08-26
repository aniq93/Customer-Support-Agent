# Import all schemas for easy access
from .user import User, UserCreate, UserUpdate, UserBase
from .ticket import Ticket, TicketCreate, TicketUpdate, TicketBase, TicketWithRequester
from .comment import Comment, CommentCreate, CommentBase, CommentWithAuthor

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserBase",
    "Ticket", "TicketCreate", "TicketUpdate", "TicketBase", "TicketWithRequester", 
    "Comment", "CommentCreate", "CommentBase", "CommentWithAuthor"
]
