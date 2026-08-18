from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.security import oauth2_scheme
from app.models.user import User, UserRole
from app.repositories.agent import AgentRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.dependencies import (
    get_agent_repository,
    get_conversation_repository,
    get_message_repository,
    get_user_repository,
)
from app.repositories.message import MessageRepository
from app.repositories.user import UserRepository
from app.services.agent import AgentService
from app.services.chat import ChatService
from app.services.jwt import JWTService
from app.services.user import UserService


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)


def get_agent_service(
    repository: AgentRepository = Depends(get_agent_repository),
) -> AgentService:
    return AgentService(repository)


def get_chat_service(
    agent_repository: AgentRepository = Depends(
        get_agent_repository,
    ),
    conversation_repository: ConversationRepository = Depends(
        get_conversation_repository,
    ),
    message_repository: MessageRepository = Depends(
        get_message_repository,
    ),
) -> ChatService:
    return ChatService(
        agent_repository=agent_repository,
        conversation_repository=conversation_repository,
        message_repository=message_repository,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    jwt_service = JWTService()

    try:
        payload = jwt_service.decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


def require_role(*allowed_roles: UserRole) -> Callable:
    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker