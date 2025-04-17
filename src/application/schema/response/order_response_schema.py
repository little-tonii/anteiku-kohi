from datetime import datetime
from typing import List
from pydantic import BaseModel

class OrderMealResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    image_url: str
    quantity: int

class CreateOrderResponse(BaseModel):
    id: int
    meals: List[OrderMealResponse]
    order_status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime

class TakeResponsibilityForOrderResponse(BaseModel):
    message: str

class UpdateOrderStatusResponse(BaseModel):
    id: int
    meals: List[OrderMealResponse]
    order_status: str
    payment_status: str
    created_at: datetime
    updated_at: datetime
