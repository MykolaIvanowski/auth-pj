from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = 'SECRET_KEY'
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRES_MINUTES = 15


def create_access_token(data: dict, expires_delta: timedelta =None ):
    to_encode = data.copy()
    expires = datetime.utcnow() + (expires_delta or timedelta(minutes=ACESS_TOKEN_EXPIRES_MINUTES))
    to_encode.update({"exp":expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

