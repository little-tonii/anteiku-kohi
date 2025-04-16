from datetime import datetime
from pydantic import BaseModel


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
    is_verified: bool

class GetUserInfoResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool
    role: str
    is_verified: bool

class LoginUserResponse(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str

class GetAccessTokenResponse(BaseModel):
    access_token: str

class VerifyAccountResponse(BaseModel):
    message: str
