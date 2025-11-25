import secrets

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.security import hash_password
from models.token import RefreshToken
from models.user import User
from schemas.user import LoginRequest, UserCreate
from schemas.token import Token, RefreshSchema
from core.security import create_access_token
from db.session import  get_db

router = APIRouter()

router.post("/login", response_model=Token)
def login(data: LoginRequest):
    ##TODO change for user check

    if data.username != "admin" or data.password != "secret":
        raise HTTPException(status_code=401, detail='sorry you are using invalid credentials')

    token = create_access_token({'sub': data.username})
    return {'access_token': token}


router.post("/refresh", response_model=Token)
def refresh_token(refresh_request: RefreshSchema, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter_by(token=refresh_request.refresh_token).first()
    if not stored or stored.revoked or stored.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token wasn't refreshed or invalid")

    stored.revoked = True
    db.commit()

    new_refresh = secrets.token_urlsafe(32)
    new_entry = RefreshToken(user_id=stored.user_id, token=new_refresh, expires_at=datetime.utcnow()+ timedelta(days=7))
    db.add(new_entry)
    db.commit()
    access = create_access_token({"sub": stored.user_id})

    return {"access_token": access, "refreshed_token": new_refresh, "token_type":"bearer"}


router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="email was registered before")
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hash_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

router.post("/logout")
def logout(refresh_request:RefreshSchema, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter_by(token=refresh_request.refreshed_token).first()

    if not stored:
        raise HTTPException(status_code=401, detail="invalid refresh token")
    stored.revoked = True
    db.commit()
    return {"message": "successfully logout!!!"}

