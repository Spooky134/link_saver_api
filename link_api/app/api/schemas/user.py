from pydantic import BaseModel, Field, field_validator, EmailStr, P
from datetime import datetime
from typing import Optional
from app.api.schemas.relations import LinkInCollection
from app.api.schemas.decorators import validate_ids_field


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserLogin(BaseModel):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True