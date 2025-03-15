from pydantic import BaseModel, field_validator


class CreateMealRequest(BaseModel):
    name: str
    description: str
    price: int
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value.strip():
            raise ValueError("Tên món ăn không được để trống")
        return value
    
    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str):
        if not value.strip():
            raise ValueError("Mô tả món ăn không được để trống")
        return value
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, value: int):
        if value <= 0:
            raise ValueError("Giá món ăn phải lớn hơn 0")
        return value