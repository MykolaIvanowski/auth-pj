import secrets
from datetime import datetime, timedelta
from tokenize import Triple

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


router.post("/refresh", responce_model=Token)
def refresh_token(refresh_request: RefreshShema, ds: Session = Depends(get_db)):
    stored =db.query(RefreshToken).filter_by(token=refresh_request.refresh_token).first()
    if not stored or stored.revoked or stored.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token wasn't refreshed or invalid")

    stored.revoked = True
    db.commit()

    new_refresh = secrets.token_urlsafe(32)
    new_entry =RefreshToken(user_id=stored.user_id, token=new_refresh, expires_at=datetime.utcnow()+ timedelta(days=7))
    db.add(new_entry)
    db.commit()
    access = create_access_token(("sub": stored.user_id})

    return {"access_token": access, "refreshed_token": new_refresh, "token_type":"bearer"}