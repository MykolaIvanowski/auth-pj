from fastapi import APIRouter, HTTPException
from app.shemes import LoginRequest, Token
from app.auth import create_access_token


router = APIRouter()

router.post("/login", response_model=Token)
def login(data: LoginRequest):
    ##TODO change for user check

    if data.username != "admin" or data.password != "secret":
        raise HTTPException(status_code=401, detail='sorry you are using invalid credentials')

    token = create_access_token({'sub': data.username})
    return {'access_token': token}
