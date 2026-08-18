from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.message import MessageRole


class MessageRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        conversation_id: int,
        role: MessageRole,
        content: str,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_conversation_messages(
        self,
        conversation_id: int,
    ) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )

        return list(
            self.db.scalars(statement).all()
        )