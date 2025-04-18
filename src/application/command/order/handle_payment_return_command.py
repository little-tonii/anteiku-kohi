from ....domain.entity.order_entity import PaymentStatus
from ....infrastructure.config.variables import VNPAY_HASH_SECRET_KEY
from ....infrastructure.utils.validate_vnpay_payment_return import validate_vnpay_payment_return
from ....application.schema.response.order_response_schema import HandlePaymentReturnResponse
from ....domain.repository.order_repository import OrderRepository
from starlette import status
from fastapi import HTTPException


class HandlePaymentReturnCommand:

    query_params: dict

    def __init__(self,
        query_params: dict
    ):
        self.query_params = query_params

class HandlePaymentReturnCommandHandler:
    order_repository: OrderRepository

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def handle(self, command: HandlePaymentReturnCommand) -> HandlePaymentReturnResponse:
        order_id = int(str(command.query_params.get("vnp_TxnRef")))
        response_code: str = str(command.query_params.get("vnp_ResponseCode"))
        bank_code: str = str(command.query_params.get("vnp_BankCode"))
        amount: int = int(str(command.query_params.get("vnp_Amount")))

        order = await self.order_repository.find_order_by_id(order_id=order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đơn hàng không tồn tại")


        if not validate_vnpay_payment_return(
            secret_key=VNPAY_HASH_SECRET_KEY,
            data=command.query_params
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=HandlePaymentReturnResponse(
                    order_id=order_id,
                    message="Thanh toán thất bại",
                    bank_code=bank_code,
                    amount=amount
                ).model_dump()
            )

        if response_code != "00":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=HandlePaymentReturnResponse(
                    order_id=order_id,
                    message="Thanh toán thất bại",
                    bank_code=bank_code,
                    amount=amount
                ).model_dump()
            )

        await self.order_repository.update_order_payment_status(order_id=order_id, status=PaymentStatus.PAID)
        await self.order_repository.delete_order_payment_url(order_id=order_id)

        return HandlePaymentReturnResponse(
            order_id=order_id,
            message="Thanh toán thành công",
            bank_code=bank_code,
            amount=amount
        )
