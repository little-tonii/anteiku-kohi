from ...domain.repository.user_repository import UserRepository
from ...application.command.manager.deactivate_user_by_email_command import DeactivateUserByEmailCommand, DeactivateUserByEmailCommandHandler
from ...application.command.manager.deactivate_user_by_id_command import DeactivateUserByIdCommand, DeactivateUserByIdCommandHandler
from ...application.schema.response.manager_response_schema import DeactivateUserResponse


class ManagerService:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    async def deactivate_user_by_id(self, role: str, id: int) -> DeactivateUserResponse:
        command = DeactivateUserByIdCommand(id=id, role=role)
        command_handler = DeactivateUserByIdCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)
    
    async def deactivate_user_by_email(self, role: str, email: str) -> DeactivateUserResponse:
        command = DeactivateUserByEmailCommand(role=role, email=email)
        command_handler = DeactivateUserByEmailCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)