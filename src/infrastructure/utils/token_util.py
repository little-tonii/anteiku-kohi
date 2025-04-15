from datetime import datetime, timedelta, timezone
from ...infrastructure.config.variables import ACCESS_TOKEN_EXPIRES, HASH_ALGORITHM, REFRESH_TOKEN_EXPIRES, SECRET_KEY
from jose import JWTError, jwt
from starlette import status
from fastapi import HTTPException

class TokenKey:
    ID: str = "id"
    EXPIRES: str = "exp"
    ROLE: str = "role"

class TokenClaims:
    id: int
    role: str

    def __init__(self, id: int, role: str):
        self.id = id
        self.role = role

def create_access_token(user_id: int, role: str) -> str:
    encode = { TokenKey.ID: user_id, TokenKey.ROLE: role }
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    encode.update({ TokenKey.EXPIRES: expires })
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)

def create_refresh_token(user_id: int, role: str) -> str:
    encode = { TokenKey.ID: user_id, TokenKey.ROLE: role }
    expires = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRES)
    encode.update({ TokenKey.EXPIRES: expires })
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)

def verify_refresh_token(refresh_token: str) -> TokenClaims:
    try:
        payload = jwt.decode(token=refresh_token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: int | None = payload.get(TokenKey.ID)
        expires: int | None = payload.get(TokenKey.EXPIRES)
        role: str | None = payload.get(TokenKey.ROLE)
        if user_id is None or role is None or expires is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        if expires and datetime.now(timezone.utc).timestamp() > expires:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
        return TokenClaims(id=user_id, role=role)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token không hợp lệ')
