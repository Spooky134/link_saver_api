from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth.dependencie import get_current_user
from app.auth.schema import UserRegister, UserLogin
from app.auth.service import AuthService
from app.exceptions import AppException
from app.user.model import UserModel

from app.dependencies import service_factory

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user_register: UserRegister, auth_service: AuthService = Depends(service_factory(AuthService))):
    try:
        await auth_service.register(user_register=user_register)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/login")
async def login(response: Response, user_login: UserLogin, auth_service: AuthService = Depends(service_factory(AuthService))):
    try:
        access_token = await auth_service.login(user_login=user_login)
        response.set_cookie(
            "link_saver_access_token",
            access_token,
            httponly=True
        )
        return {"access_token": access_token}
    except AppException as e:
        return HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/logout")
async def logout(response: Response):
    try:
        response.delete_cookie("link_saver_access_token")
        # await auth_service.logout()
        return {"message": "Logged out"}
    except AppException as e:
        return HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/me")
async def users_me(current_user: UserModel = Depends(get_current_user)):
    try:
        return current_user
    except AppException as e:
        return HTTPException(status_code=404, detail=str(e))

