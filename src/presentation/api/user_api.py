from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from ...infrastructure.config.security import verify_access_token

from ...infrastructure.utils.token_util import TokenClaims

from ...infrastructure.config.dependencies import get_user_service

from ...application.schema.request.user_request_schema import GetAccessTokenRequest, LogoutUserRequest, RegisterUserRequest

from ...application.schema.response.user_response_schema import GetAccessTokenResponse, GetUserInfoResponse, LoginUserResponse, RegisterUserResponse
from ...application.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])

@router.delete(path="/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(claims: Annotated[TokenClaims, Depends(verify_access_token)], user_service: Annotated[UserService, Depends(get_user_service)], request: LogoutUserRequest):
    await user_service.logout_user(refresh_token=request.refresh_token)

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
    
@router.post(path="/refresh", status_code=status.HTTP_200_OK, response_model=GetAccessTokenResponse)
async def get_access_token(user_service: Annotated[UserService, Depends(get_user_service)], request: GetAccessTokenRequest):
    return await user_service.create_access_token(refresh_token=request.refresh_token)

@router.get(path="/info", status_code=status.HTTP_200_OK, response_model=GetUserInfoResponse)
async def get_info(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_user_info(id=claims.id)