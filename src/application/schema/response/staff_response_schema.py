from datetime import datetime
from pydantic import BaseModel


class GetStaffByIdResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    address: str
    updated_at: datetime
    joined_at: datetime
    is_active: bool