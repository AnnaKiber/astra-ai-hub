from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User, UserRole
from app.schemas import Token, UserCreate, UserResponse
from app.services.auth import get_current_user
from app.services.dependencies import get_user_service
from app.services.permissions import require_role
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.register(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    try:
        token = service.login(
            email=form_data.username,
            password=form_data.password,
        )

        return Token(
            access_token=token,
            token_type="bearer",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/admin",
    response_model=UserResponse,
)
def admin_endpoint(
    current_user: User = Depends(
        require_role(UserRole.ADMIN),
    ),
):
    return current_user