from ...application.command.manager.activate_user_by_email_command import ActivateUserByEmailCommand, ActivateUserByEmailCommandHandler
from ...application.command.manager.activate_user_by_id_command import ActivateUserByIdCommand, ActivateUserByIdCommandHandler
from ...domain.repository.user_repository import UserRepository
from ...application.command.manager.deactivate_user_by_email_command import DeactivateUserByEmailCommand, DeactivateUserByEmailCommandHandler
from ...application.command.manager.deactivate_user_by_id_command import DeactivateUserByIdCommand, DeactivateUserByIdCommandHandler
from ...application.schema.response.manager_response_schema import ActivateUserResponse, DeactivateUserResponse


class ManagerService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def deactivate_user_by_id(self, role: str, user_id: int, manager_id: int) -> DeactivateUserResponse:
        command = DeactivateUserByIdCommand(
            current_manager_id=manager_id,
            user_id=user_id,
            role=role,
        )
        command_handler = DeactivateUserByIdCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)

    async def deactivate_user_by_email(self, role: str, email: str) -> DeactivateUserResponse:
        command = DeactivateUserByEmailCommand(role=role, email=email)
        command_handler = DeactivateUserByEmailCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)

    async def activate_user_by_id(self, role: str, id: int) -> ActivateUserResponse:
        command = ActivateUserByIdCommand(id=id, role=role)
        command_handler = ActivateUserByIdCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)

    async def activate_user_by_email(self, role: str, email: str) -> ActivateUserResponse:
        command = ActivateUserByEmailCommand(role=role, email=email)
        command_handler = ActivateUserByEmailCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)
