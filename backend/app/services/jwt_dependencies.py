from app.services.jwt import JWTService


def get_jwt_service() -> JWTService:
    return JWTService()