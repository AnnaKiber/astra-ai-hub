from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        owner_id: int,
        agent_id: int,
    ) -> Conversation:
        conversation = Conversation(
            owner_id=owner_id,
            agent_id=agent_id,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
        )

        return self.db.scalar(statement)