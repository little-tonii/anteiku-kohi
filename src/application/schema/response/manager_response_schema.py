from pydantic import BaseModel


class DeactivateUserResponse(BaseModel):
    message: str
    
class ActivateUserResponse(BaseModel):
    message: str