from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import InvalidTokenError

from app.core.config import settings


class JWTService:
    """
    Сервис для создания и проверки JWT-токенов.
    """

    def create_access_token(
        self,
        data: dict[str, Any],
    ) -> str:
        payload = data.copy()

        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload["exp"] = expire

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def decode_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except InvalidTokenError:
            raise ValueError("Invalid token")