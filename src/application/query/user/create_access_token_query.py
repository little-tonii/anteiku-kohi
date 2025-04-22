from fastapi import HTTPException
from ....infrastructure.utils.token_util import create_access_token, verify_refresh_token
from ....application.schema.response.user_response_schema import GetAccessTokenResponse
from ....domain.repository.user_repository import UserRepository
from starlette import status

class CreateAccessTokenQuery:
    refresh_token: str

    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

class CreateAccessTokenQueryHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, query: CreateAccessTokenQuery) -> GetAccessTokenResponse:
        claims = verify_refresh_token(refresh_token=query.refresh_token)
        user_entity = await self.user_repository.get_by_id(id=claims.id)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ")
        if user_entity.refresh_token != query.refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ")
        if user_entity.is_active == False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản đã bị vô hiệu hóa")
        access_token = create_access_token(user_id=user_entity.id, role=user_entity.role)
        return GetAccessTokenResponse(access_token=access_token)
