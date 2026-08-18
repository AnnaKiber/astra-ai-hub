from app.models.agent import Agent
from app.repositories.agent import AgentRepository
from app.schemas.agent import (
    AgentCreate,
    AgentUpdate,
)


class AgentService:
    def __init__(
        self,
        repository: AgentRepository,
    ):
        self.repository = repository

    def create(
        self,
        agent: AgentCreate,
        owner_id: int,
    ) -> Agent:
        return self.repository.create(
            agent=agent,
            owner_id=owner_id,
        )

    def get_by_id(
        self,
        agent_id: int,
    ) -> Agent:
        agent = self.repository.get_by_id(agent_id)

        if agent is None:
            raise ValueError("Agent not found")

        return agent

    def get_all(
        self,
    ) -> list[Agent]:
        return self.repository.get_all()

    def update(
        self,
        agent_id: int,
        agent_data: AgentUpdate,
    ) -> Agent:
        agent = self.repository.get_by_id(agent_id)

        if agent is None:
            raise ValueError("Agent not found")

        return self.repository.update(
            db_agent=agent,
            agent=agent_data,
        )

    def delete(
        self,
        agent_id: int,
    ) -> None:
        agent = self.repository.get_by_id(agent_id)

        if agent is None:
            raise ValueError("Agent not found")

        self.repository.delete(agent)