from fastapi import HTTPException
from ....application.schema.response.manager_response_schema import ActivateUserResponse
from ....domain.entity.user_entity import UserRole
from ....domain.repository.user_repository import UserRepository
from ....infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl
from starlette import status

class ActivateUserByEmailCommand:
    role: str
    email: str
    
    def __init__(self, email: str, role: str):
        self.email = email
        self.role = role
        
class ActivateUserByEmailCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository
        
    async def handle(self, command: ActivateUserByEmailCommand) -> ActivateUserResponse:
        if command.role != UserRole.MANAGER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        success = await self.user_repository.activate_by_email(email=command.email)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại hoặc chưa bị vô hiệu hoá")
        return ActivateUserResponse(message="Kích hoạt người dùng thành công")