from fastapi import HTTPException
from ....domain.repository.user_repository import UserRepository
from starlette import status

class LogoutUserCommand:
    refresh_token: str
    
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token
        
class LogoutUserCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def handle(self, command: LogoutUserCommand) -> None:
        user_entity = await self.user_repository.get_by_refresh_token(refresh_token=command.refresh_token)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ")
        user_entity.refresh_token = None
        await self.user_repository.update(user_entity=user_entity)