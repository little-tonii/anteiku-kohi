from typing import Annotated
from fastapi import APIRouter, Depends

from ...infrastructure.utils.validator import validate_email, validate_user_id

from ...application.service.manager_service import ManagerService

from ...application.schema.response.manager_response_schema import ActivateUserResponse, DeactivateUserResponse

from ...infrastructure.config.dependencies import get_manager_service

from ...infrastructure.config.security import verify_access_token
from ...infrastructure.utils.token_util import TokenClaims
from starlette import status

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.post(path="/deactivate-user/id/{id}", status_code=status.HTTP_200_OK, response_model=DeactivateUserResponse)
async def deactivate_user_by_id(
    claims: Annotated[TokenClaims, Depends(verify_access_token)], 
    manager_service: Annotated[ManagerService, Depends(get_manager_service)], 
    id: Annotated[int, Depends(validate_user_id)]
):
    return await manager_service.deactivate_user_by_id(role=claims.role, id=id)

@router.post(path="/deactivate-user/email/{email}", status_code=status.HTTP_200_OK, response_model=DeactivateUserResponse)
async def deactivate_user_by_email(
    claims: Annotated[TokenClaims, Depends(verify_access_token)], 
    manager_service: Annotated[ManagerService, Depends(get_manager_service)], 
    email: Annotated[str, Depends(validate_email)]
):
    return await manager_service.deactivate_user_by_email(role=claims.role, email=email)

@router.post(path="/activate-user/id/{id}", status_code=status.HTTP_200_OK, response_model=ActivateUserResponse)
async def activate_user_by_id(
    claims: Annotated[TokenClaims, Depends(verify_access_token)], 
    manager_service: Annotated[ManagerService, Depends(get_manager_service)], 
    id: Annotated[int, Depends(validate_user_id)]
):
    return await manager_service.activate_user_by_id(role=claims.role, id=id)

@router.post(path="/activate-user/email/{email}", status_code=status.HTTP_200_OK, response_model=ActivateUserResponse)
async def activate_user_by_email(
    claims: Annotated[TokenClaims, Depends(verify_access_token)], 
    manager_service: Annotated[ManagerService, Depends(get_manager_service)], 
    email: Annotated[str, Depends(validate_email)]
):
    return await manager_service.activate_user_by_email(role=claims.role, email=email)