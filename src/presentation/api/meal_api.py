from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from fastapi_cache.coder import JsonCoder
from starlette import status
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from ...infrastructure.config.caching import RedisNamespace
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
    id: int,
    background_tasks: BackgroundTasks,
):
    response = await meal_service.enable_meal(id=id)
    background_tasks.add_task(FastAPICache.clear, namespace=RedisNamespace.MEAL_LIST)
    background_tasks.add_task(FastAPICache.clear, namespace=f"{RedisNamespace.MEAL}:{id}")
    return response

@router.patch(path="/disable/{id}", status_code=status.HTTP_200_OK, response_model=DisableMealResponse)
async def disable_meal(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    id: int,
    background_tasks: BackgroundTasks,
):
    response = await meal_service.disable_meal(id=id)
    background_tasks.add_task(FastAPICache.clear, namespace=RedisNamespace.MEAL_LIST)
    background_tasks.add_task(FastAPICache.clear, namespace=f"{RedisNamespace.MEAL}:{id}")
    return response

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=CreateMealResponse)
async def create_meal(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    background_tasks: BackgroundTasks,
    name: str = Depends(validate_meal_name),
    description: str = Depends(validate_meal_description),
    price: int = Depends(validate_meal_price),
    picture: UploadFile = Depends(validate_picture),
):
    response = await meal_service.create_meal(
        name=name,
        description=description,
        price=price,
        picture=picture
    )
    background_tasks.add_task(FastAPICache.clear, namespace=RedisNamespace.MEAL_LIST)
    return response

@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=GetMealResponse)
@cache(
    expire=60 * 60 * 24,
    namespace=RedisNamespace.MEAL,
    coder=JsonCoder,
    key_builder=lambda func, namespace="", *, request=None, response=None, args=(), kwargs={}: (
        ":".join([
            namespace,
            str(kwargs.get('id'))
        ])
    )
)
async def get_meal_by_id(meal_service: Annotated[MealService, Depends(get_meal_service)], id: int):
    return await meal_service.get_meal_by_id(id=id)

@router.get(path="/", status_code=status.HTTP_200_OK, response_model=GetMealsResponse)
@cache(
    expire=60 * 60 * 24,
    namespace=RedisNamespace.MEAL_LIST,
    coder=JsonCoder,
    key_builder=lambda func, namespace="", *, request=None, response=None, args=(), kwargs={}: (
        ":".join([
            namespace,
            str(kwargs.get('page')),
            str(kwargs.get('size')),
            'all' if kwargs.get('is_available') is None else str(kwargs.get('is_available'))
        ])
    )
)
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
    request: UpdateMealDataRequest,
    background_tasks: BackgroundTasks,
):
    response = await meal_service.update_meal_data(
        id=id,
        name=request.name,
        description=request.description,
        price=request.price
    )
    background_tasks.add_task(FastAPICache.clear, namespace=RedisNamespace.MEAL_LIST)
    background_tasks.add_task(FastAPICache.clear, namespace=f"{RedisNamespace.MEAL}:{id}")
    return response

@router.put(path="/update-image/{id}", status_code=status.HTTP_200_OK, response_model=UpdateMealImageResponse)
async def update_meal_image(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    meal_service: Annotated[MealService, Depends(get_meal_service)],
    background_tasks: BackgroundTasks,
    id: int,
    picture: UploadFile = Depends(validate_picture)
):
    response = await meal_service.update_meal_image(id=id, picture=picture)
    background_tasks.add_task(FastAPICache.clear, namespace=RedisNamespace.MEAL_LIST)
    background_tasks.add_task(FastAPICache.clear, namespace=f"{RedisNamespace.MEAL}:{id}")
    return response
