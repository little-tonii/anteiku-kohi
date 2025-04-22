from fastapi import HTTPException
from ....application.schema.response.manager_response_schema import ActivateUserResponse
from ....domain.entity.user_entity import UserRole
from ....domain.repository.user_repository import UserRepository
from starlette import status

class ActivateUserByIdCommand:
    role: str
    id: int

    def __init__(self, id: int, role: str):
        self.id = id
        self.role = role

class ActivateUserByIdCommandHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: ActivateUserByIdCommand) -> ActivateUserResponse:
        if command.role != UserRole.MANAGER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
        success = await self.user_repository.activate_by_id(id=command.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại hoặc chưa bị vô hiệu hoá")
        return ActivateUserResponse(message="Kích hoạt người dùng thành công")
