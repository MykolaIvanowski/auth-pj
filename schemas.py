from pydantic import BaseModel

class Token(BaseModel):
    access_token : str
    token_type : str="bearer"

class LoginRequest:
    username: str
    password: str
