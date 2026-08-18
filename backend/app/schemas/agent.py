from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.agent import ModelProvider


class AgentBase(BaseModel):
    name: str
    description: str
    system_prompt: str
    model: ModelProvider = ModelProvider.GPT_4_1_MINI
    temperature: float = 0.7
    is_public: bool = False


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    system_prompt: str | None = None
    model: ModelProvider | None = None
    temperature: float | None = None
    is_public: bool | None = None


class AgentResponse(AgentBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )