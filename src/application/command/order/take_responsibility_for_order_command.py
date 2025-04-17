from ....application.schema.response.order_response_schema import TakeResponsibilityForOrderResponse
from ....domain.repository.order_repository import OrderRepository
from fastapi import HTTPException
from starlette import status


class TakeResponsibilityForOrderCommand:
    order_id: int
    staff_id: int

    def __init__(self, order_id: int, staff_id: int):
        self.order_id = order_id
        self.staff_id = staff_id

class TakeResponsibilityForOrderCommandHandler:
    order_repository: OrderRepository

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def handle(self, command: TakeResponsibilityForOrderCommand) -> TakeResponsibilityForOrderResponse:
        existed_order = await self.order_repository.find_order_by_id(order_id=command.order_id)
        if not existed_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đơn hàng không tồn tại")
        if existed_order.staff_id == command.staff_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bạn đang chịu trách nhiệm xử lý đơn hàng này")
        request_result = await self.order_repository.update_order_staff_id(
            order_id=command.order_id,
            staff_id=command.staff_id,
        )
        if request_result:
            return TakeResponsibilityForOrderResponse(message="Chịu trách nhiệm xử lý đơn hàng thành công")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Đơn hàng đã được chịu trách nhiệm xử lý bởi nhân viên khác")
