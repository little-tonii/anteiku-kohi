from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile
from starlette import status

from ...application.schema.request.meal_request_schema import UpdateMealDataRequest

from ...infrastructure.utils.validator import validate_is_available_meal, validate_meal_description, validate_meal_name, validate_meal_price, validate_page, validate_picture, validate_size

from ...application.schema.response.meal_response_schema import CreateMealResponse, DisableMealResponse, EnableMealResponse, GetMealResponse, GetMealsResponse, UpdateMealDataResponse, UpdateMealImageResponse
from ...application.service.meal_service import MealService
from ...infrastructure.config.dependencies import get_meal_service
from ...infrastructure.config.security import verify_access_token
from ...infrastructure.utils.token_util import TokenClaims

router = APIRouter(prefix="/meal", tags=["Meal"])

@router.patch(path="/enable/{id}", status_code=status.HTTP_200_OK, response_model=EnableMealResponse)
async def enable_meal(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    id: int
):
    return await meal_service.enable_meal(id=id)

@router.patch(path="/disable/{id}", status_code=status.HTTP_200_OK, response_model=DisableMealResponse)
async def disable_meal(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    id: int
):
    return await meal_service.disable_meal(id=id)

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=CreateMealResponse)
async def create_meal(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    name: str = Depends(validate_meal_name),
    description: str = Depends(validate_meal_description),
    price: int = Depends(validate_meal_price),
    picture: UploadFile = Depends(validate_picture)
):
    return await meal_service.create_meal(
        name=name,
        description=description,
        price=price,
        picture=picture
    )

@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=GetMealResponse)
async def get_meal_by_id(meal_service: Annotated[MealService, Depends(get_meal_service)], id: int):
    return await meal_service.get_meal_by_id(id=id)

@router.get(path="/", status_code=status.HTTP_200_OK, response_model=GetMealsResponse)
async def get_meals(
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    size: int = Depends(validate_size),
    page: int = Depends(validate_page),
    is_available: bool | None = Depends(validate_is_available_meal)
):
    return await meal_service.get_meals(page=page, size=size, is_available=is_available)

@router.patch(path="/update-data/{id}", status_code=status.HTTP_200_OK, response_model=UpdateMealDataResponse)
async def update_meal_data(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    id: int,
    request: UpdateMealDataRequest
):
    return await meal_service.update_meal_data(
        id=id,
        name=request.name,
        description=request.description,
        price=request.price
    )

@router.put(path="/update-image/{id}", status_code=status.HTTP_200_OK, response_model=UpdateMealImageResponse)
async def update_meal_image(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    id: int,
    picture: UploadFile = Depends(validate_picture)
):
    return await meal_service.update_meal_image(id=id, picture=picture)
