from fastapi import HTTPException
from ....application.schema.response.manager_response_schema import DeactivateUserResponse
from ....domain.entity.user_entity import UserRole
from ....domain.repository.user_repository import UserRepository
from starlette import status

class DeactivateUserByEmailCommand:
    email: str
    role: str
    current_manager_id: int

    def __init__(self, email: str, role: str, current_manager_id: int):
        self.email = email
        self.role = role
        self.current_manager_id = current_manager_id

class DeactivateUserByEmailCommandHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: DeactivateUserByEmailCommand) -> DeactivateUserResponse:
        if command.role != UserRole.MANAGER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        user_entity = await self.user_repository.get_by_email(email=command.email)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại hoặc đã bị vô hiệu hoá")
        if user_entity.id == command.current_manager_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không thể vô hiệu hoá chính mình")
        success = await self.user_repository.deactivate_by_email(email=command.email)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại hoặc đã bị vô hiệu hoá")
        return DeactivateUserResponse(message="Vô hiệu hoá người dùng thành công")
