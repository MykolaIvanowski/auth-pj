from sqlmodel import Session, select
from models import AuthUser
from security import hash_password


def create_user(session: Session, email: str, password:str) -> AuthUser:
    user = AuthUser(email=email,hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session:Session, email:str ) -> AuthUser:
    return session.exec(select(AuthUser).where(AuthUser.email == email )).first()