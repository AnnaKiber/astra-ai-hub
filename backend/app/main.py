from fastapi import FastAPI

from app.api.router import router

app = FastAPI(
    title="Astra AI Platform",
    description="AI Business Platform API",
    version="1.0.0",
)

app.include_router(router)