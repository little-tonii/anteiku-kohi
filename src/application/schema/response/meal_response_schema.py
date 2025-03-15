from datetime import datetime

from pydantic import BaseModel


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