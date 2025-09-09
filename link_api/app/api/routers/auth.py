from fastapi import Depends, APIRouter, HTTPException, status, Query
from typing import Optional
from link_api.app.api.schemas.user import (
    UserCreate,
    UserResponse,
    # UserUpdate,
    # LoginRequest,
    # TokenResponse,
    # PasswordResetRequest
)
from app.services.auth import AuthService
from app.api.dependencies import service_factory
from app.exceptions.exceptions import ValidationError

router = APIRouter(prefix="/auth", tags=["auth"])

# Регистрация и активация
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, service: AuthService = Depends(service_factory(AuthService))):
    try:
        return await service.register_user(user_data=user_create)
    except ValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    

@router.post("/login", response_model=TokenResponse)
async def login(login_request: LoginRequest, service: AuthService = Depends(service_factory(AuthService))):
    try:
        return await service.login(
            username=login_request.username,
            password=login_request.password
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str = Query(...), service: AuthService = Depends(service_factory(AuthService))):
    try:
        return await service.refresh_tokens(refresh_token=refresh_token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    

@router.post("/logout", status_code=status)
async def refresh_token(refresh_token: str = Query(...), service: AuthService = Depends(service_factory(AuthService))):
    try:
        return await service.refresh_tokens(refresh_token=refresh_token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Query(...), service: AuthService = Depends(service_factory(AuthService))):
    # try:
    return await service.get_current_user(token=token)
    # except UnauthorizedError as e:
    #     raise HTTPException(status_code=e.status_code, detail=e.detail)







# TODO сделать верификацию почты
# @router.get("/verify-email/{token}", response_model=UserResponse)
# async def verify_email(token: str, service: AuthService = Depends(service_factory(AuthService))):
#     try:
#         return await service.verify_email(token=token)
#     except ValidationError as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# # Аутентификация






