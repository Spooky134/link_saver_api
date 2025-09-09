from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.api.schemas.relations import LinkInCollection
from app.api.schemas.decorators import validate_ids_field




class TokenBase(BaseModel):
    token_type: str = "bearer"


class TokenResponse(TokenBase):
    access_token: str
    refresh_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "550e8400-e29b-41d4-a716-446655440000",
                "token_type": "bearer"
            }
        }