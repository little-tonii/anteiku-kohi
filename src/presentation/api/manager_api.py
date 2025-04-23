from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_limiter.depends import RateLimiter
from starlette import status

from ...infrastructure.config.rate_limiting import identifier_based_on_claims
from ...application.service.user_service import UserService
from ...infrastructure.config.caching import REDIS_PREFIX, FastAPICacheExtended, RedisNamespace
from ...infrastructure.utils.validator import validate_email, validate_user_id
from ...application.service.manager_service import ManagerService
from ...application.schema.response.manager_response_schema import ActivateUserResponse, DeactivateUserResponse
from ...infrastructure.config.dependencies import get_manager_service, get_user_service
from ...infrastructure.config.security import verify_access_token
from ...infrastructure.utils.token_util import TokenClaims

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.patch(
    path="/deactivate-user/id/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DeactivateUserResponse,
    dependencies=[
        Depends(verify_access_token),
        Depends(RateLimiter(times=3, seconds=60, identifier=identifier_based_on_claims))
    ]
)
async def deactivate_user_by_id(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    manager_service: Annotated[ManagerService, Depends(get_manager_service)],
    id: Annotated[int, Depends(validate_user_id)],
    background_tasks: BackgroundTasks,
):
    response = await manager_service.deactivate_user_by_id(role=claims.role, user_id=id, manager_id=claims.id)
    background_tasks.add_task(FastAPICacheExtended.clear, key=":".join([REDIS_PREFIX, RedisNamespace.USER, str(id)]))
    return response

@router.patch(
    path="/deactivate-user/email/{email}",
    status_code=status.HTTP_200_OK,
    response_model=DeactivateUserResponse,
    dependencies=[
        Depends(verify_access_token),
        Depends(RateLimiter(times=3, seconds=60, identifier=identifier_based_on_claims))
    ]
)
async def deactivate_user_by_email(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    manager_service: Annotated[ManagerService, Depends(get_manager_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    email: Annotated[str, Depends(validate_email)],
    background_tasks: BackgroundTasks,
):
    user_response = await user_service.get_user_by_email(email=email)
    deactivate_response = await manager_service.deactivate_user_by_email(role=claims.role, email=email, manager_id=claims.id)
    background_tasks.add_task(FastAPICacheExtended.clear, key=":".join([REDIS_PREFIX, RedisNamespace.USER, str(user_response.id)]))
    return deactivate_response

@router.patch(
    path="/activate-user/id/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ActivateUserResponse,
    dependencies=[
        Depends(verify_access_token),
        Depends(RateLimiter(times=3, seconds=60, identifier=identifier_based_on_claims))
    ]
)
async def activate_user_by_id(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    manager_service: Annotated[ManagerService, Depends(get_manager_service)],
    id: Annotated[int, Depends(validate_user_id)]
):
    return await manager_service.activate_user_by_id(role=claims.role, id=id)

@router.patch(
    path="/activate-user/email/{email}",
    status_code=status.HTTP_200_OK,
    response_model=ActivateUserResponse,
    dependencies=[
        Depends(verify_access_token),
        Depends(RateLimiter(times=3, seconds=60, identifier=identifier_based_on_claims))
    ]
)
async def activate_user_by_email(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    manager_service: Annotated[ManagerService, Depends(get_manager_service)],
    email: Annotated[str, Depends(validate_email)]
):
    return await manager_service.activate_user_by_email(role=claims.role, email=email)
