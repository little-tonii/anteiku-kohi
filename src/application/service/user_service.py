from ...application.query.user.create_access_token_query import CreateAccessTokenQuery, CreateAccessTokenQueryHandler
from ...application.command.user.logout_user_command import LogoutUserCommand, LogoutUserCommandHandler
from ...domain.repository.user_repository import UserRepository
from ...application.command.user.register_user_command import RegisterUserCommand, RegisterUserCommandHandler

from ...application.command.user.login_user_command import LoginUserCommand, LoginUserCommandHandler
from ...application.schema.response.user_response_schema import GetAccessTokenResponse, LoginUserResponse, RegisterUserResponse

class UserService:
    
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    async def logout_user(self, refresh_token: str) -> None:
        command = LogoutUserCommand(refresh_token=refresh_token)
        command_handler = LogoutUserCommandHandler(user_repository=self.user_repository)
        await command_handler.handle(command=command)
        
    async def login_user(self, email: str, password: str) -> LoginUserResponse:
        command = LoginUserCommand(email=email, password=password)
        command_handler = LoginUserCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)
    
    async def register_user(self, full_name: str, phone_number: str, email: str, address: str, password: str) -> RegisterUserResponse:
        command = RegisterUserCommand(
            address=address,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            password=password
        )
        command_handler = RegisterUserCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)
    
    async def create_access_token(self, refresh_token: str) -> GetAccessTokenResponse:
        query = CreateAccessTokenQuery(refresh_token=refresh_token)
        query_handler = CreateAccessTokenQueryHandler(user_repository=self.user_repository)
        return await query_handler.handle(query=query)