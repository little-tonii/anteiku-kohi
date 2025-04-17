from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from ...infrastructure.config.security import verify_access_token
from ...infrastructure.utils.token_util import TokenClaims
from ...application.service.order_service import OrderService
from ...infrastructure.config.dependencies import get_order_service
from ...application.schema.request.order_request_schema import CreateOrderRequest, UpdateOrderStatusRequest
from ...application.schema.response.order_response_schema import CreateOrderResponse, TakeResponsibilityForOrderResponse, UpdateOrderStatusResponse

router = APIRouter(prefix="/order", tags=["Order"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CreateOrderResponse)
async def create_order(
    request: CreateOrderRequest,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.create_order(meals_ids=request.meals)

@router.put("/take-responsibility", status_code=status.HTTP_200_OK, response_model=TakeResponsibilityForOrderResponse)
async def take_responsibility_for_order(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    order_id: int,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.take_responsibility_for_order(order_id=order_id, staff_id=claims.id)

@router.put("/update-status", status_code=status.HTTP_200_OK, response_model=UpdateOrderStatusResponse)
async def update_order_status(
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
    request: UpdateOrderStatusRequest,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.update_order_status(order_id=request.order_id, staff_id=claims.id, status=request.status)
