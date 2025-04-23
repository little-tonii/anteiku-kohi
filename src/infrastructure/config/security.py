from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from ...infrastructure.config.dependencies import get_user_repository

from ...domain.repository.user_repository import UserRepository
from ...infrastructure.config.variables import HASH_ALGORITHM, SECRET_KEY
from ...infrastructure.utils.token_util import TokenClaims, TokenKey
from jose import JWTError, jwt
from starlette import status

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='user/login')

async def verify_access_token(request: Request, token: Annotated[str, Depends(oauth2_bearer)], user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> TokenClaims:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: int | None = payload.get(TokenKey.ID)
        expires: int | None = payload.get(TokenKey.EXPIRES)
        user_role: str | None = payload.get(TokenKey.ROLE)
        if user_id is None or user_role is None or expires is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if datetime.now(timezone.utc).timestamp() > expires:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if await user_repository.get_by_id(id=user_id) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        claims = TokenClaims(id=user_id, role=user_role)
        request.state.claims = claims
        return claims
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
