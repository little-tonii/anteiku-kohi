from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from ...infrastructure.config.dependencies import get_user_service

from ...application.schema.request.user_request_schema import RegisterUserRequest

from ...application.schema.response.user_response_schema import LoginUserResponse, RegisterUserResponse
from ...application.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])

@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=LoginUserResponse)
async def login(user_service: Annotated[UserService, Depends(get_user_service)], login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await user_service.login_user(email=login_form.username, password=login_form.password)

@router.post(path="/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse)
async def register(user_service: Annotated[UserService, Depends(get_user_service)], request: RegisterUserRequest):
    return await user_service.register_user(
        full_name=request.full_name,
        phone_number=request.phone_number,
        email=request.email,
        address=request.address,
        password=request.password
    )