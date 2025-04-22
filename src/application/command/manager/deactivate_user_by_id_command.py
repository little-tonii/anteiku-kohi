from fastapi import HTTPException

from ....application.schema.response.manager_response_schema import DeactivateUserResponse
from ....domain.entity.user_entity import UserRole
from ....domain.repository.user_repository import UserRepository
from starlette import status

class DeactivateUserByIdCommand:
    user_id: int
    role: str
    current_manager_id: int

    def __init__(self, user_id: int, role: str, current_manager_id: int):
        self.user_id = user_id
        self.role = role
        self.current_manager_id = current_manager_id

class DeactivateUserByIdCommandHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: DeactivateUserByIdCommand) -> DeactivateUserResponse:
        if command.role != UserRole.MANAGER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        if command.current_manager_id == command.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể tự vô hiệu hóa chính mình")
        success = await self.user_repository.deactivate_by_id(id=command.user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại hoặc đã bị vô hiệu hoá")
        return DeactivateUserResponse(message="Vô hiệu hoá người dùng thành công")
