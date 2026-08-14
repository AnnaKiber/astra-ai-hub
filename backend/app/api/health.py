from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Astra AI Platform"
    }


@router.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok"
    }