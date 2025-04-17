from datetime import datetime
from typing import Optional


class OrderStatus:
    READY = "READY"
    DELIVERED = "DELIVERED"
    ONQUEUE = "ONQUEUE"
    CANCELLED = "CANCELLED"
    PROCESSING = "PROCESSING"

class PaymentStatus:
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"

class OrderEntity:
    id: int
    meals: list[int]
    order_status: str
    created_at: datetime
    updated_at: datetime
    payment_status: str
    staff_id: Optional[int]

    def __init__(
        self,
        id: int,
        meals: list[int],
        order_status: str,
        created_at: datetime,
        updated_at: datetime,
        payment_status: str,
        staff_id: Optional[int] = None
    ):
        self.id = id
        self.meals = meals
        self.order_status = order_status
        self.created_at = created_at
        self.updated_at = updated_at
        self.payment_status = payment_status
        self.staff_id = staff_id
