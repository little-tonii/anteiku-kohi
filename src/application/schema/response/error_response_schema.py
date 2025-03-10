from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    
class ErrorsResponse(BaseModel):
    messages: list[str]