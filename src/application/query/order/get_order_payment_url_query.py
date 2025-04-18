from fastapi import HTTPException
from datetime import datetime
from ....domain.entity.order_entity import PaymentStatus

from ....infrastructure.utils.create_payment_url import create_payment_url

from ....infrastructure.config.variables import VNPAY_RETURN_URL, VNPAY_TMN_CODE, VNPAY_HASH_SECRET_KEY, VNPAY_PAYMENT_URL
from ....application.schema.response.order_response_schema import GetOrderPaymentUrlResponse
from ....domain.repository.order_repository import OrderRepository
from starlette import status

class GetOrderPaymentUrlQuery:
    order_id: int
    client_ip_address: str

    def __init__(self, order_id: int, client_ip_address: str):
        self.order_id = order_id
        self.client_ip_address = client_ip_address


class GetOrderPaymentUrlQueryHandler:
    order_repository: OrderRepository

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def handle(self, query: GetOrderPaymentUrlQuery) -> GetOrderPaymentUrlResponse:
        order = await self.order_repository.find_order_by_id(order_id=query.order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đơn hàng không tồn tại")
        if order.payment_status == PaymentStatus.PAID:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Đơn hàng đã được thanh toán")
        if order.payment_status == PaymentStatus.REFUNDED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Đơn hàng đã được hoàn tiền")
        order_meals = await self.order_repository.get_order_meal_list(order_id=query.order_id)
        payment_url_params = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': VNPAY_TMN_CODE,
            'vnp_Amount': sum(order_meal.price * order_meal.quantity for order_meal in order_meals) * 100,
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': f'{order.created_at.strftime("%Y%m%d%H%M%S")}-{order.id}',
            'vnp_OrderInfo': f'Anteiku Kohi - Mã hóa đơn {order.id}',
            'vnp_OrderType': 'Thanh toán hóa đơn',
            'vnp_Locale': 'vn',
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_IpAddr': query.client_ip_address,
            'vnp_ReturnUrl': VNPAY_RETURN_URL
        }
        payment_url = create_payment_url(
           vnpay_url_params=payment_url_params,
           vnpay_hash_secret_key=VNPAY_HASH_SECRET_KEY,
           vnpay_payment_url=VNPAY_PAYMENT_URL
        )
        return GetOrderPaymentUrlResponse(payment_url=payment_url)
