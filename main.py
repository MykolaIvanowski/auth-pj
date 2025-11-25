from fastapi import FastAPI
from core.logging import LoggingMiddleware
from routers import auth as auth_router


app = FastAPI(
    title='start auth service',
    description="Microservice for authentications with JWT and refresh tokens",
    version="0.1.1")


app.include_router(auth_router, prefix='/auth', tags=["auth-pj"])
app.middleware(LoggingMiddleware)
