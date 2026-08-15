from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user import UserRepository


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)