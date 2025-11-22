from fastapi import FastAPI
from routers import auth as auth_router

app = FastAPI(title='start auth service')
app.include_router(auth_router, prefix='/auth')
