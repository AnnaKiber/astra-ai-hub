from fastapi import Depends, HTTPException, status

from app.models.user import User, UserRole
from app.services.auth import get_current_user


def require_role(*roles: UserRole):
    def checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user

    return checker