import re
from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError

class LogoutUserRequest(BaseModel):
    refresh_token: str

    @field_validator("refresh_token")
    @classmethod
    def validate_refresh_token(cls, value: str):
        if not value.strip():
            raise ValueError("Refresh token không được để trống")
        return value.strip()

class RegisterUserRequest(BaseModel):
    email: str
    password: str
    full_name: str
    address: str
    phone_number: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        if not value.strip():
            raise ValueError("Email không được để trống")
        try:
            email_infor = validate_email(value, check_deliverability=True)
            return email_infor.normalized.lower()
        except EmailNotValidError:
            raise ValueError(f"Email {value} không hợp lệ")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not value.strip():
            raise ValueError("Mật khẩu không được để trống")
        if len(value) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
        return value

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):
        cleaned_name = value.strip()
        if not cleaned_name:
            raise ValueError("Họ và tên không được để trống")
        return cleaned_name.strip()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        phone_pattern = re.compile(r"^(0\d{9}|\+84\d{9})$")
        if not phone_pattern.match(value):
            raise ValueError("Số điện thoại không hợp lệ")
        return value.strip()

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str):
        if not value.strip():
            raise ValueError("Địa chỉ không được để trống")
        return value.strip()

class GetAccessTokenRequest(BaseModel):
    refresh_token: str

    @field_validator("refresh_token")
    @classmethod
    def validate_refresh_token(cls, value: str):
        if not value.strip():
            raise ValueError("Refresh token không được để trống")
        return value.strip()

class ForgotPasswordRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        if value.strip() == "":
            raise ValueError("Email không được để trống")
        try:
            email_infor = validate_email(value, check_deliverability=True)
            return email_infor.normalized.lower()
        except EmailNotValidError:
            raise ValueError(f"Email {value} không hợp lệ")

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        if value.strip() == "":
            raise ValueError("Email không được để trống")
        try:
            email_infor = validate_email(value, check_deliverability=True)
            return email_infor.normalized.lower()
        except EmailNotValidError:
            raise ValueError(f"Email {value} không hợp lệ")

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str):
        if value.strip() == "":
            raise ValueError("Mã xác nhận không được để trống")
        return value.strip()

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str):
        if len(value) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
        return value
