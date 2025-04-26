from concurrent.futures import ProcessPoolExecutor
from typing import List
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from ..repository_impl.reset_password_code_repository_impl import ResetPasswordCodeRepositoryImpl
from ...domain.repository.reset_password_code_repository import ResetPasswordCodeRepository
from ...application.service.order_service import OrderService
from ...application.service.manager_service import ManagerService
from ...application.service.meal_service import MealService
from ...domain.repository.meal_repository import MealRepository
from ..repository_impl.meal_repository_impl import MealRepositoryImpl
from ...application.service.user_service import UserService
from ..repository_impl.user_repository_impl import UserRepositoryImpl
from ...domain.repository.user_repository import UserRepository
from ..config.database import AsyncSessionLocal
from ...domain.repository.order_repository import OrderRepository
from ..repository_impl.order_repository_impl import OrderRepositoryImpl

# database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# process pool executer
def get_process_executor(request: Request) -> ProcessPoolExecutor:
    return request.app.state.process_executor

# redlock connection manager
def get_redlock_connection_manager(request: Request) -> List[Redis]:
    return request.app.state.redlock_connection_manager

# repository dependecies
def get_user_repository(async_session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(async_session=async_session)

def get_meal_repository(async_session: AsyncSession = Depends(get_db)) -> MealRepository:
    return MealRepositoryImpl(async_session=async_session)

def get_order_repository(async_session: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepositoryImpl(async_session=async_session)

def get_reset_password_code_repository(async_session: AsyncSession = Depends(get_db)) -> ResetPasswordCodeRepository:
    return ResetPasswordCodeRepositoryImpl(async_session=async_session)

# service dependencies
def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    reset_password_code_repository: ResetPasswordCodeRepository = Depends(get_reset_password_code_repository),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        reset_password_code_repository=reset_password_code_repository,
    )

def get_manager_service(user_repository: UserRepository = Depends(get_user_repository)) -> ManagerService:
    return ManagerService(user_repository=user_repository)

def get_meal_service(
    meal_repository: MealRepository = Depends(get_meal_repository),
    process_executor: ProcessPoolExecutor = Depends(get_process_executor),
    redlock_connection_manager: List[Redis] = Depends(get_redlock_connection_manager)
) -> MealService:
    return MealService(
        meal_repository=meal_repository,
        process_executor=process_executor,
        redlock_connection_manager=redlock_connection_manager
    )

def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
    meal_repository: MealRepository = Depends(get_meal_repository)
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        meal_repository=meal_repository,
    )
