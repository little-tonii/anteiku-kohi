from pydantic import BaseModel


class DeactivateUserResponse(BaseModel):
    message: str