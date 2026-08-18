from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.agent import AgentRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository
from app.repositories.user import UserRepository


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_agent_repository(
    db: Session = Depends(get_db),
) -> AgentRepository:
    return AgentRepository(db)


def get_conversation_repository(
    db: Session = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)


def get_message_repository(
    db: Session = Depends(get_db),
) -> MessageRepository:
    return MessageRepository(db)