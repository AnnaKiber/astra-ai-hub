from app.models.agent import Agent
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.repositories.agent import AgentRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository


class ChatService:
    def __init__(
        self,
        agent_repository: AgentRepository,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ):
        self.agent_repository = agent_repository
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    def create_conversation(
        self,
        owner_id: int,
        agent_id: int,
    ) -> Conversation:
        agent = self.agent_repository.get_by_id(agent_id)

        if agent is None:
            raise ValueError("Agent not found")

        return self.conversation_repository.create(
            owner_id=owner_id,
            agent_id=agent_id,
        )

    def add_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> Message:
        conversation = self.conversation_repository.get_by_id(
            conversation_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        return self.message_repository.create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=content,
        )

    def add_assistant_message(
        self,
        conversation_id: int,
        content: str,
    ) -> Message:
        conversation = self.conversation_repository.get_by_id(
            conversation_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        return self.message_repository.create(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=content,
        )

    def get_messages(
        self,
        conversation_id: int,
    ) -> list[Message]:
        conversation = self.conversation_repository.get_by_id(
            conversation_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        return self.message_repository.get_conversation_messages(
            conversation_id,
        )