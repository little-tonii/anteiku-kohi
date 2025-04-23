from fastapi import HTTPException, Request, Response
from starlette import status

async def http_callback_exception_handler(request: Request, response: Response, pexpire: int):
    expire = pexpire / 1000
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Bạn đã vượt quá giới hạn số lượng truy cập. Vui lòng thử lại sau.",
        headers={"Retry-After": str(expire)}
    )
