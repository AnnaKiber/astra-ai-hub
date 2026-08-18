from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    agent_id: int


class ConversationResponse(BaseModel):
    id: int
    owner_id: int
    agent_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )