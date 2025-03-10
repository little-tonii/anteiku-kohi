from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from application.schema.response.error_response_schema import ErrorResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    message = exc.detail
    return JSONResponse(
        status_code=exc.status_code, 
        content=ErrorResponse(message=message).model_dump()
    )
    
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, 
        content=ErrorResponse(message=f"Có lỗi xảy ra").model_dump()
    )