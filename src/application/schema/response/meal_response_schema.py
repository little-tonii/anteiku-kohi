from datetime import datetime

from pydantic import BaseModel

from ....domain.entity.meal_entity import MealEntity


class GetMealResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_available: bool
    price: int
    image_url: str

class GetMealsResponse(BaseModel):
    meals: list[GetMealResponse]
    page: int
    size: int
        
class CreateMealResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_available: bool
    price: int
    image_url: str
    
class DisableMealResponse(BaseModel):
    message: str
    
class EnableMealResponse(BaseModel):
    message: str
    
class UpdateMealDataResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_available: bool
    price: int
    
class UpdateMealImageResponse(BaseModel):
    id: int
    image_url: str