from pydantic import BaseModel, Field, field_validator, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
#
#     class Config:
#         from_attributes = True
#         json_schema_extra = {
#             "example": {
#                 "email": "user@example.com",
#                 "password": "securepassword123"
#             }
#         }
#
#
# class UserLogin(BaseModel):
#     pass