from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.service.meal_service import MealService

from ...domain.repository.meal_repository import MealRepository
from ...infrastructure.repository_impl.meal_repository_impl import MealRepositoryImpl

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

def get_meal_repository(async_session: AsyncSession = Depends(get_db)) -> MealRepository:
    return MealRepositoryImpl(async_session=async_session)

# service dependencies
def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)

def get_meal_service(meal_repository: MealRepository = Depends(get_meal_repository)) -> MealService:
    return MealService(meal_repository=meal_repository)