from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache import JsonCoder
from starlette import status
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter

from ...application.background_task.send_email_reset_password_code import send_email_reset_password_code
from ...application.background_task.send_email_reset_password_success import send_email_reset_password_success
from ...infrastructure.config.rate_limiting import identifier_based_on_claims
from ...infrastructure.config.caching import RedisNamespace
from ...infrastructure.config.security import verify_access_token
from ...infrastructure.utils.token_util import TokenClaims
from ...infrastructure.config.dependencies import get_user_service
from ...application.schema.request.user_request_schema import ForgotPasswordRequest, GetAccessTokenRequest, LogoutUserRequest, RegisterUserRequest, ResetPasswordRequest
from ...application.schema.response.user_response_schema import ForgotPasswordResponse, GetAccessTokenResponse, GetUserInfoResponse, LoginUserResponse, RegisterUserResponse, ResetPasswordResponse, VerifyAccountResponse
from ...application.service.user_service import UserService
from ...application.background_task.send_email_verification import send_email_verification

router = APIRouter(prefix="/user", tags=["User"])

@router.delete(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(verify_access_token),
        Depends(RateLimiter(times=20, seconds=60, identifier=identifier_based_on_claims))
    ]
)
async def logout(
    user_service: Annotated[UserService, Depends(get_user_service)],
    request: LogoutUserRequest
):
    await user_service.logout_user(refresh_token=request.refresh_token)

@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginUserResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def login(
    user_service: Annotated[UserService, Depends(get_user_service)],
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await user_service.login_user(email=login_form.username, password=login_form.password)

@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterUserResponse,
    dependencies=[Depends(RateLimiter(times=3, seconds=60))]
)
async def register(
    user_service: Annotated[UserService, Depends(get_user_service)],
    request: RegisterUserRequest,
    background_tasks: BackgroundTasks
):
    response = await user_service.register_user(
        full_name=request.full_name,
        phone_number=request.phone_number,
        email=request.email,
        address=request.address,
        password=request.password
    )
    background_tasks.add_task(send_email_verification, response.email)
    return response

@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    response_model=GetAccessTokenResponse,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def get_access_token(user_service: Annotated[UserService, Depends(get_user_service)], request: GetAccessTokenRequest):
    return await user_service.create_access_token(refresh_token=request.refresh_token)

@router.get(
    path="/info",
    status_code=status.HTTP_200_OK,
    response_model=GetUserInfoResponse,
    dependencies=[
        Depends(verify_access_token),
        Depends(RateLimiter(times=20, seconds=60, identifier=identifier_based_on_claims))
    ]
)
@cache(
    namespace=RedisNamespace.USER,
    expire=60 * 60 * 24 * 7,
    coder=JsonCoder,
    key_builder=lambda func, namespace="", *, request=None, response=None, args=(), kwargs={}: (
        ":".join([
            namespace,
            str(kwargs['claims'].id),
        ])
    )
)
async def get_info(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_user_info(id=claims.id)

@router.get(
    path="/email-verification/{token}",
    status_code=status.HTTP_200_OK,
    response_model=VerifyAccountResponse,
    dependencies=[Depends(RateLimiter(times=5, minutes=10))]
)
async def verify_account(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token: str
):
    return await user_service.verify_account(token=token)

@router.post(
    path="/forgot-password",
    status_code=status.HTTP_201_CREATED,
    response_model=ForgotPasswordResponse,
    dependencies=[Depends(RateLimiter(times=3, seconds=60))]
)
async def forgot_password(
    user_service: Annotated[UserService, Depends(get_user_service)],
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
):
    response = await user_service.create_reset_password_code(email=request.email)
    background_tasks.add_task(send_email_reset_password_code, email=response.user_email, code=response.code)
    return response

@router.post(
    path="/reset-password",
    status_code=status.HTTP_200_OK,
    response_model=ResetPasswordResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def reset_password(
    user_service: Annotated[UserService, Depends(get_user_service)],
    request: ResetPasswordRequest,
    background_tasks: BackgroundTasks,
):
    response = await user_service.reset_password(email=request.email, code=request.code, new_password=request.new_password)
    background_tasks.add_task(send_email_reset_password_success, email=request.email)
    return response
