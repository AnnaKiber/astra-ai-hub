from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate


class AgentRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        agent: AgentCreate,
        owner_id: int,
    ) -> Agent:
        db_agent = Agent(
            **agent.model_dump(),
            owner_id=owner_id,
        )

        self.db.add(db_agent)
        self.db.commit()
        self.db.refresh(db_agent)

        return db_agent

    def get_by_id(
        self,
        agent_id: int,
    ) -> Agent | None:
        statement = select(Agent).where(
            Agent.id == agent_id,
        )
        return self.db.scalar(statement)

    def get_all(self) -> list[Agent]:
        statement = select(Agent)
        return list(self.db.scalars(statement).all())

    def update(
        self,
        db_agent: Agent,
        agent: AgentUpdate,
    ) -> Agent:
        for key, value in agent.model_dump(
            exclude_unset=True,
        ).items():
            setattr(db_agent, key, value)

        self.db.commit()
        self.db.refresh(db_agent)

        return db_agent

    def delete(
        self,
        db_agent: Agent,
    ) -> None:
        self.db.delete(db_agent)
        self.db.commit()