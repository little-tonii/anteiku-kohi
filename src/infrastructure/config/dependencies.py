from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.service.user_service import UserService

from ...application.command.user.register_user_command import RegisterUserCommandHandler

from ...application.command.user.login_user_command import LoginUserCommandHandler
from ...infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl
from ...domain.repository.user_repository import UserRepository
from ...infrastructure.config.database import AsyncSessionLocal

# database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            
# repository dependecies
def get_user_repository(async_session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(async_session=async_session)

# cqrs dependencies
def get_login_user_command_handler(user_repository: UserRepository = Depends(get_user_repository)) -> LoginUserCommandHandler:
    return LoginUserCommandHandler(user_repository=user_repository)

def get_register_user_command_handler(user_repository: UserRepository = Depends(get_user_repository)) -> RegisterUserCommandHandler:
    return RegisterUserCommandHandler(user_repository=user_repository)

# service dependencies
def get_user_service(
    login_user_command_handler: LoginUserCommandHandler = Depends(get_login_user_command_handler),
    register_user_command_handler: RegisterUserCommandHandler = Depends(get_register_user_command_handler)
) -> UserService:
    return UserService(
        login_user_command_handler=login_user_command_handler,
        register_user_command_handler=register_user_command_handler
    )