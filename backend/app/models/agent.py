from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class ModelProvider(str, Enum):
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        default="",
        nullable=False,
    )

    system_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    model: Mapped[ModelProvider] = mapped_column(
        SQLEnum(
            ModelProvider,
            values_callable=lambda enum: [item.value for item in enum],
        ),
        default=ModelProvider.GPT_4_1_MINI,
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.7,
        nullable=False,
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="agents",
    )