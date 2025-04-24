from concurrent.futures import ThreadPoolExecutor
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.service.order_service import OrderService
from ...application.service.manager_service import ManagerService
from ...application.service.meal_service import MealService
from ...domain.repository.meal_repository import MealRepository
from ...infrastructure.repository_impl.meal_repository_impl import MealRepositoryImpl
from ...application.service.user_service import UserService
from ...infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl
from ...domain.repository.user_repository import UserRepository
from ...infrastructure.config.database import AsyncSessionLocal
from ...domain.repository.order_repository import OrderRepository
from ...infrastructure.repository_impl.order_repository_impl import OrderRepositoryImpl

# database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# thread pool executer
def get_thread_executor(request: Request) -> ThreadPoolExecutor:
    return request.app.state.thread_executor

# repository dependecies
def get_user_repository(async_session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(async_session=async_session)

def get_meal_repository(async_session: AsyncSession = Depends(get_db)) -> MealRepository:
    return MealRepositoryImpl(async_session=async_session)

def get_order_repository(async_session: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepositoryImpl(async_session=async_session)

# service dependencies
def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)

def get_manager_service(user_repository: UserRepository = Depends(get_user_repository)) -> ManagerService:
    return ManagerService(user_repository=user_repository)

def get_meal_service(
    meal_repository: MealRepository = Depends(get_meal_repository),
    thread_executor: ThreadPoolExecutor = Depends(get_thread_executor)
) -> MealService:
    return MealService(meal_repository=meal_repository, thread_executor=thread_executor)

def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
    meal_repository: MealRepository = Depends(get_meal_repository)
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        meal_repository=meal_repository,
    )
