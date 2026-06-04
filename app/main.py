from fastapi import FastAPI
from app.core.logging import LoggingMiddleware
from app.routers.auth import router as auth_router

app = FastAPI(
    title='start auth service',
    description="Microservice for authentications with JWT and refresh tokens",
    version="0.1.1")


app.include_router(auth_router, prefix='/auth', tags=["auth-pj"])
app.middleware(LoggingMiddleware)
