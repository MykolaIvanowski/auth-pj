from pydantic import BaseModel


class Token(BaseModel):
    access_token : str
    refresh_token: str
    token_type : str="bearer"


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra={ "example": {
            "email" : "test@email.com",
            "password": "thisisrealstrongpasword12345"
        }
    }


class RefreshSchema(BaseModel):
    refreshed_token : str