from ...application.command.user.register_user_command import RegisterUserCommand, RegisterUserCommandHandler

from ...application.command.user.login_user_command import LoginUserCommand, LoginUserCommandHandler
from ...application.schema.response.user_response_schema import LoginUserResponse, RegisterUserResponse

class UserService:
    
    login_user_command_handler: LoginUserCommandHandler
    register_user_command_handler: RegisterUserCommandHandler
    
    def __init__(
        self, 
        login_user_command_handler: LoginUserCommandHandler,
        register_user_command_handler: RegisterUserCommandHandler
    ):
        self.login_user_command_handler = login_user_command_handler
        self.register_user_command_handler = register_user_command_handler
    
    async def login_user(self, email: str, password: str) -> LoginUserResponse:
        command = LoginUserCommand(email=email, password=password)
        return await self.login_user_command_handler.handle(command=command)
    
    async def register_user(self, full_name: str, phone_number: str, email: str, address: str, password: str) -> RegisterUserResponse:
        command = RegisterUserCommand(
            address=address,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            password=password
        )
        return await self.register_user_command_handler.handle(command=command)