from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.jwt import JWTService
from app.services.password import (
    hash_password,
    verify_password,
)


class UserService:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository
        self.jwt_service = JWTService()

    def register(
        self,
        user_data: UserCreate,
    ) -> User:
        existing_user = self.repository.get_by_email(
            user_data.email,
        )

        if existing_user:
            raise ValueError("User already exists")

        hashed_password = hash_password(
            user_data.password,
        )

        return self.repository.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
        )

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = self.repository.get_by_email(email)

        if user is None:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    def login(
        self,
        email: str,
        password: str,
    ) -> str:
        user = self.authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise ValueError(
                "Invalid email or password",
            )

        return self.jwt_service.create_access_token(
            {
                "sub": str(user.id),
            }
        )