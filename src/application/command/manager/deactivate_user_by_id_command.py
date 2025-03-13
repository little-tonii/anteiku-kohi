from fastapi import HTTPException

from ....application.schema.response.manager_response_schema import DeactivateUserResponse
from ....domain.entity.user_entity import UserRole
from ....infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl
from ....domain.repository.user_repository import UserRepository
from starlette import status

class DeactivateUserByIdCommand:
    id: int
    role: str
    
    def __init__(self, id: int, role: str):
        self.id = id
        self.role = role
        
class DeactivateUserByIdCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository
        
    async def handle(self, command: DeactivateUserByIdCommand) -> DeactivateUserResponse:
        if command.role != UserRole.MANAGER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        success = await self.user_repository.deactivate_by_id(id=command.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại hoặc đã bị vô hiệu hoá")
        return DeactivateUserResponse(message="Vô hiệu hoá người dùng thành công")