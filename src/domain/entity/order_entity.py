from datetime import datetime


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
    total: int
    created_at: datetime
    updated_at: datetime
    payment_status: str
    staff_id: int
    
    def __init__(
        self, 
        id: int, 
        meals: list[int],
        status: str, 
        total: int, 
        created_at: datetime,
        updated_at: datetime,
        payment_status: str
    ):
        self.id = id
        self.meals = meals
        self.status = status
        self.total = total
        self.created_at = created_at
        self.updated_at = updated_at
        self.payment_status = payment_status