from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str