from datetime import datetime
from pydantic import BaseModel, Field

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
    user_email: str = Field(exclude=True)

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
    is_verified: bool

class ForgotPasswordResponse(BaseModel):
    message: str
    user_id: int = Field(exclude=True)
    code: str = Field(exclude=True)
    user_email: str = Field(exclude=True)

class ResetPasswordResponse(BaseModel):
    message: str
