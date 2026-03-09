from fastapi import APIRouter, Response, status
from pydantic import EmailStr

from app.auth.dependencies import AuthServiceDep, CurrentUserDep
from app.auth.schemas import (
    AccessToken,
    ChangePassword,
    MessageResponse,
    ResetPasswordRequest,
    UserLogin,
    UserRegister,
)
from app.user.entities import CreateUserEntity

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
async def register(data: UserRegister, auth_service: AuthServiceDep):
    user_register = CreateUserEntity(**data.model_dump())
    await auth_service.register(user_register)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def login(response: Response, data: UserLogin, auth_service: AuthServiceDep):
    access_token = await auth_service.login(str(data.email), data.password)
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def logout(response: Response, _: CurrentUserDep):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.post(
    "/change_password", response_model=MessageResponse, status_code=status.HTTP_200_OK
)
async def change_password(
    data: ChangePassword, auth_service: AuthServiceDep, current_user: CurrentUserDep
):
    await auth_service.change_password(
        current_user.id, data.old_password, data.new_password
    )

    return {"message": "Password changed successfully"}


@router.post(
    "/password-reset-request",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def password_reset_request(email: EmailStr, auth_service: AuthServiceDep):
    await auth_service.request_password_reset(str(email))
    return {"message": "If the email exists, a reset link was sent"}


@router.post(
    "/password-reset", response_model=MessageResponse, status_code=status.HTTP_200_OK
)
async def password_reset(data: ResetPasswordRequest, auth_service: AuthServiceDep):
    await auth_service.reset_password(
        reset_token=data.token, new_password=data.new_password
    )
    return {"message": "Password successfully reset"}
