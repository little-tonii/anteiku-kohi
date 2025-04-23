from typing import cast
from fastapi import Request, HTTPException, Response
from starlette import status

from ..utils.token_util import TokenClaims

RATE_LIMITTING_CACHE_PREFIX = "rate_limiting_cache"

async def http_callback_exception_handler(request: Request, response: Response, pexpire: int):
    expire = pexpire / 1000
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Vượt quá giới hạn lưu lượng truy cập. Vui lòng thử lại sau.",
        headers={"Retry-After": str(expire)}
    )

async def identifier_based_on_claims(request: Request) -> str:
    return str(cast(TokenClaims, request.state.claims).id)
