from fastapi import APIRouter, Depends, Response
from app.auth.schemas import UserRegister, UserLogin
from app.user.entities import UserEntity
from app.user.models import UserModel
from app.auth.dependencies import AuthServiceDep, get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=None)
async def register(user_register: UserRegister, auth_service: AuthServiceDep):
    user_register = UserEntity(**user_register.model_dump())
    await auth_service.register(user_register=user_register)


@router.post("/login")
async def login(response: Response, user_login: UserLogin, auth_service: AuthServiceDep):
    access_token = await auth_service.login(user_login=user_login)
    response.set_cookie(
        "link_saver_access_token",
        access_token,
        httponly=True
    )
    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("link_saver_access_token")
    # await auth_service.logout()
    return {"message": "Logged out"}


@router.get("/me")
async def users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
