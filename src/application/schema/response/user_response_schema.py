from datetime import datetime
from pydantic import BaseModel

class LogoutUserResponse(BaseModel):
    message: str

class RegisterUserResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool
    role: str

class GetUserByIdResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool
    role: str
    
class GetUserByEmailResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool
    role: str
    
class LoginUserResponse(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str