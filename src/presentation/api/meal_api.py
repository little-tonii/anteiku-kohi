from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from ...application.schema.request.meal_request_schema import CreateMealRequest
from ...application.schema.response.meal_response_schema import CreateMealResponse
from ...application.service.meal_service import MealService
from ...infrastructure.config.dependencies import get_meal_service
from ...infrastructure.config.security import verify_access_token
from ...infrastructure.utils.token_util import TokenClaims

router = APIRouter(prefix="/meal", tags=["Meal"])

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=CreateMealResponse)
async def create_meal(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    request: CreateMealRequest
):
    return await meal_service.create_meal(
        name=request.name, 
        description=request.description, 
        price=request.price
    )