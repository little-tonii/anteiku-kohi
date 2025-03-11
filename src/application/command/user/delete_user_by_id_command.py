from fastapi import Depends, HTTPException
from domain.repository.user_repository import UserRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl

class DeleteUserByIdCommand:
    id: int
    
    def __init__(self, id: int):
        self.id = id
        
class DeleteUserByIdCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl = Depends()):
        self.user_repository = user_repository
        
    async def handle(self, command: DeleteUserByIdCommand) -> None:
        success = await self.user_repository.delete_by_id(id=command.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhân viên không tồn tại")