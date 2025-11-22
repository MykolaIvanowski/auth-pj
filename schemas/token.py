from pydantic import BaseModel


class Token(BaseModel):
    access_token : str
    refresh_token: str
    token_type : str="bearer"


class LoginSchema(BaseModel):
    email: str
    password: str


class RefreshSchema(BaseModel):
    refreshed_token : str