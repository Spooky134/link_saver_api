from fastapi import APIRouter, Response
from fastapi import status
from app.auth.schemas import UserRegister, UserLogin, AccessToken, MessageResponse
from app.user.entities import UserEntity, CreateUserEntity
from app.auth.dependencies import AuthServiceDep


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(user_register: UserRegister, auth_service: AuthServiceDep):
    user_register = CreateUserEntity(**user_register.model_dump())
    await auth_service.register(user_register)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def login(response: Response, user_login: UserLogin, auth_service: AuthServiceDep):
    access_token = await auth_service.login(
        str(user_login.email),
        user_login.password
    )
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True
    )
    return {"access_token": access_token}


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}



