from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(UserRegister):
    pass

class AccessToken(BaseModel):
    access_token: str

class MessageResponse(BaseModel):
    message: str