from fastapi import Depends, HTTPException
from ....domain.repository.user_repository import UserRepository
from starlette import status

from ....infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl

class DeleteUserByEmailCommand:
    email: str
    
    def __init__(self, email: str):
        self.email = email
        
class DeleteUserByEmailCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl = Depends()):
        self.user_repository = user_repository
        
    async def handle(self, command: DeleteUserByEmailCommand) -> None:
        success = await self.user_repository.delete_by_email(email=command.email)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhân viên không tồn tại")