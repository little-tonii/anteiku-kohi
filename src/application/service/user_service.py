from ...application.command.user.reset_password_command import ResetPasswordCommand, ResetPasswordCommandHandler
from ...domain.repository.reset_password_code_repository import ResetPasswordCodeRepository
from ...application.command.user.create_reset_password_code_command import CreateResetPasswordCodeCommand, CreateResetPasswordCodeCommandHandler
from ...application.query.user.get_user_by_email_query import GetUserByEmailQuery, GetUserByEmailQueryHandler
from ...application.query.user.get_user_info_query import GetUserInfoQuery, GetUserInfoQueryHandler
from ...application.query.user.create_access_token_query import CreateAccessTokenQuery, CreateAccessTokenQueryHandler
from ...application.command.user.logout_user_command import LogoutUserCommand, LogoutUserCommandHandler
from ...domain.repository.user_repository import UserRepository
from ...application.command.user.register_user_command import RegisterUserCommand, RegisterUserCommandHandler
from ...application.command.user.verify_account_command import VerifyAccountCommand, VerifyAccountCommandHandler
from ...application.command.user.login_user_command import LoginUserCommand, LoginUserCommandHandler
from ...application.schema.response.user_response_schema import (
    ForgotPasswordResponse,
    GetUserByEmailResponse,
    ResetPasswordResponse,
    VerifyAccountResponse,
    GetAccessTokenResponse,
    GetUserInfoResponse,
    LoginUserResponse,
    RegisterUserResponse
)

class UserService:

    user_repository: UserRepository
    reset_password_code_repository: ResetPasswordCodeRepository

    def __init__(
        self,
        user_repository: UserRepository,
        reset_password_code_repository: ResetPasswordCodeRepository,
    ):
        self.user_repository = user_repository
        self.reset_password_code_repository = reset_password_code_repository

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

    async def get_user_info(self, id: int) -> GetUserInfoResponse:
        query = GetUserInfoQuery(id=id)
        query_handler = GetUserInfoQueryHandler(user_repository=self.user_repository)
        return await query_handler.handle(query=query)

    async def verify_account(self, token: str) -> VerifyAccountResponse:
        command = VerifyAccountCommand(token=token)
        command_handler = VerifyAccountCommandHandler(user_repository=self.user_repository)
        return await command_handler.handle(command=command)

    async def get_user_by_email(self, email: str) -> GetUserByEmailResponse:
        query = GetUserByEmailQuery(email=email)
        query_handler = GetUserByEmailQueryHandler(user_repository=self.user_repository)
        return await query_handler.handle(query=query)

    async def create_reset_password_code(self, email: str) -> ForgotPasswordResponse:
        command = CreateResetPasswordCodeCommand(email=email)
        command_handler = CreateResetPasswordCodeCommandHandler(
            user_repository=self.user_repository,
            reset_password_code_repository=self.reset_password_code_repository,
        )
        return await command_handler.handle(command=command)

    async def reset_password(self, email: str, code: str, new_password: str) -> ResetPasswordResponse:
        command = ResetPasswordCommand(email=email, code=code, new_password=new_password)
        command_handler = ResetPasswordCommandHandler(
            user_repository=self.user_repository,
            reset_password_code_repository=self.reset_password_code_repository,
        )
        return await command_handler.handle(command=command)
