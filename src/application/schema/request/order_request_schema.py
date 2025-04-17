from typing import List
from pydantic import BaseModel, field_validator


class CreateOrderRequest(BaseModel):
    meals: List[int]

    @field_validator("meals")
    @classmethod
    def validate_meals(cls, value: List[int]):
        if len(value) == 0:
            raise ValueError("Phải chọn ít nhất một món ăn")
        return value

class TakeResponsibilityForOrderRequest(BaseModel):
    order_id: int

    @field_validator("order_id")
    @classmethod
    def validate_order_id(cls, value: int):
        if value <= 0:
            raise ValueError("Mã đơn hàng không hợp lệ")
        return value

class UpdateOrderStatusRequest(BaseModel):
    order_id: int
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str):
        if value.strip().upper() not in ["READY", "DELIVERED", "ONQUEUE", "CANCELLED", "PROCESSING"]:
            raise ValueError("Trạng thái đơn hàng không hợp lệ")
        return value.strip().upper()

    @field_validator("order_id")
    @classmethod
    def validate_order_id(cls, value: int):
        if value <= 0:
            raise ValueError("Mã đơn hàng không hợp lệ")
        return value
