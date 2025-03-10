from datetime import datetime
from pydantic import BaseModel

class UpdateUserResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool

class CreateUserResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool

class GetUserByIdResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool
    
class GetUserByEmailResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool