from fastapi import HTTPException
from ....application.schema.response.order_response_schema import GetOrderPaymentUrlResponse
from ....domain.repository.order_repository import OrderRepository
from starlette import status

class GetOrderPaymentUrlQuery:
    order_id: int

    def __init__(self, order_id: int):
        self.order_id = order_id


class GetOrderPaymentUrlQueryHandler:
    order_repository: OrderRepository

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def handle(self, query: GetOrderPaymentUrlQuery) -> GetOrderPaymentUrlResponse:
        order = await self.order_repository.find_order_by_id(order_id=query.order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đơn hàng không tồn tại")
        if order.payment_url is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Đơn hàng không khả dụng để thanh toán")
        return GetOrderPaymentUrlResponse(payment_url=order.payment_url)
