from typing import Optional

from sqlalchemy import select, update
from ...domain.entity.user_entity import UserEntity
from ...domain.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ...infrastructure.model.user_model import UserModel, UserRole

class UserRepositoryImpl(UserRepository):
    async_session: AsyncSession

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def activate_by_id(self, id: int) -> bool:
        async with self.async_session as session:
            query = (
                update(UserModel)
                .where(UserModel.id == id, UserModel.role == UserRole.STAFF, UserModel.is_active == False)
                .values(is_active=True)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def activate_by_email(self, email: str) -> bool:
        async with self.async_session as session:
            query = (
                update(UserModel)
                .where(UserModel.email == email, UserModel.role == UserRole.STAFF, UserModel.is_active == False)
                .values(is_active=True)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def get_by_refresh_token(self, refresh_token: str) -> Optional[UserEntity]:
        async with self.async_session as session:
            query = select(UserModel).where(UserModel.refresh_token == refresh_token)
            query_result = await session.execute(query)
            user_model = query_result.scalar_one_or_none()
            if not user_model:
                return None
            return UserEntity(
                id=user_model.id, # type: ignore
                full_name=user_model.full_name, # type: ignore
                phone_number=user_model.phone_number, # type: ignore
                email=user_model.email, # type: ignore
                address=user_model.address, # type: ignore
                updated_at=user_model.updated_at, # type: ignore
                joined_at=user_model.joined_at, # type: ignore
                is_active=user_model.is_active, # type: ignore
                hashed_password=user_model.hashed_password, # type: ignore
                refresh_token=user_model.refresh_token, # type: ignore
                role=user_model.role, # type: ignore
                is_verified=user_model.is_verified # type: ignore
            )

    async def get_by_id(self, id: int) -> Optional[UserEntity]:
        async with self.async_session as session:
            query = select(UserModel).where(UserModel.id == id, UserModel.is_active == True)
            query_result = await session.execute(query)
            user_model = query_result.scalar_one_or_none()
            if not user_model:
                return None
            return UserEntity(
                id=user_model.id, # type: ignore
                full_name=user_model.full_name, # type: ignore
                phone_number=user_model.phone_number, # type: ignore
                email=user_model.email, # type: ignore
                address=user_model.address, # type: ignore
                updated_at=user_model.updated_at, # type: ignore
                joined_at=user_model.joined_at, # type: ignore
                is_active=user_model.is_active, # type: ignore
                hashed_password=user_model.hashed_password, # type: ignore
                refresh_token=user_model.refresh_token, # type: ignore
                role=user_model.role, # type: ignore
                is_verified=user_model.is_verified # type: ignore
            )

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        async with self.async_session as session:
            query = select(UserModel).where(UserModel.email == email, UserModel.is_active == True)
            query_result = await session.execute(query)
            user_model = query_result.scalar_one_or_none()
            if not user_model:
                return None
            return UserEntity(
                id=user_model.id, # type: ignore
                full_name=user_model.full_name, # type: ignore
                phone_number=user_model.phone_number, # type: ignore
                email=user_model.email, # type: ignore
                address=user_model.address, # type: ignore
                updated_at=user_model.updated_at, # type: ignore
                joined_at=user_model.joined_at, # type: ignore
                is_active=user_model.is_active, # type: ignore
                hashed_password=user_model.hashed_password, # type: ignore
                refresh_token=user_model.refresh_token, # type: ignore
                role=user_model.role, # type: ignore
                is_verified=user_model.is_verified # type: ignore
            )

    async def deactivate_by_id(self, id: int) -> bool:
        async with self.async_session as session:
            query = (
                update(UserModel)
                .where(UserModel.id == id, UserModel.role == UserRole.STAFF, UserModel.is_active == True)
                .values(is_active=False)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def deactivate_by_email(self, email: str) -> bool:
        async with self.async_session as session:
            query = (
                update(UserModel)
                .where(UserModel.email == email, UserModel.role == UserRole.STAFF, UserModel.is_active == True)
                .values(is_active=False)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def create(self, full_name: str, phone_number: str, email: str, address: str, hashed_password: str) -> UserEntity:
        async with self.async_session as session:
            async with session.begin():
                user_model = UserModel(
                    full_name=full_name,
                    phone_number=phone_number,
                    email=email,
                    address=address,
                    hashed_password=hashed_password
                )
                session.add(user_model)
                await session.flush()
            await session.refresh(user_model)
            return UserEntity(
                id=user_model.id, # type: ignore
                full_name=user_model.full_name, # type: ignore
                phone_number=user_model.phone_number, # type: ignore
                email=user_model.email, # type: ignore
                address=user_model.address, # type: ignore
                updated_at=user_model.updated_at, # type: ignore
                joined_at=user_model.joined_at, # type: ignore
                is_active=user_model.is_active, # type: ignore
                hashed_password=user_model.hashed_password, # type: ignore
                refresh_token=user_model.refresh_token, # type: ignore
                role=user_model.role, # type: ignore
                is_verified=user_model.is_verified # type: ignore
            )

    async def update(self, user_entity: UserEntity) -> Optional[UserEntity]:
        async with self.async_session as session:
            async with session.begin():
                query = (
                    update(UserModel)
                    .where(UserModel.id == user_entity.id)
                    .values(
                        full_name=user_entity.full_name,
                        phone_number=user_entity.phone_number,
                        address=user_entity.address,
                        hashed_password=user_entity.hashed_password,
                        refresh_token=user_entity.refresh_token,
                        is_verified=user_entity.is_verified
                    )
                    .returning(UserModel)
                )
                result = await session.execute(query)
                user_model = result.scalar_one_or_none()
                if user_model is None:
                    return None
            return UserEntity(
                id=user_model.id, # type: ignore
                full_name=user_model.full_name, # type: ignore
                phone_number=user_model.phone_number, # type: ignore
                email=user_model.email, # type: ignore
                address=user_model.address, # type: ignore
                updated_at=user_model.updated_at, # type: ignore
                joined_at=user_model.joined_at, # type: ignore
                is_active=user_model.is_active, # type: ignore
                hashed_password=user_model.hashed_password, # type: ignore
                refresh_token=user_model.refresh_token, # type: ignore
                role=user_model.role, # type: ignore
                is_verified=user_model.is_verified # type: ignore
            )
