from typing import Optional
from pydantic import BaseModel, field_validator


class UpdateMealDataRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]):
        if value is not None and not value.strip():
            raise ValueError("Tên món ăn không được để trống")
        elif value is not None:
            return value.strip()
        else:
            return None

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]):
        if value is not None and not value.strip():
            raise ValueError("Mô tả món ăn không được để trống")
        elif value is not None:
            return value.strip()
        else:
            return None

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Optional[int]):
        if value is not None and value <= 0:
            raise ValueError("Giá món ăn phải lớn hơn 0")
        return value
