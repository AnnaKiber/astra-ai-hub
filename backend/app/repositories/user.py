from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Репозиторий для работы с пользователями."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        email: str,
        username: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)