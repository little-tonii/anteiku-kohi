from typing import Optional

from sqlalchemy import select, update
from ...domain.entity.user_entity import UserEntity
from ...domain.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ...infrastructure.model.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    async_session: AsyncSession
    
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
        
    async def get_by_id(self, id: int) -> Optional[UserEntity]:
        async with self.async_session as session:
            query = select(UserModel).where(UserModel.id == id, UserModel.is_active == True)
            query_result = await session.execute(query)
            user_model = query_result.scalar_one_or_none()
            if not user_model:
                return None
            return UserEntity(
                id=user_model.id,
                full_name=user_model.full_name,
                phone_number=user_model.phone_number,
                email=user_model.email,
                address=user_model.address,
                updated_at=user_model.updated_at,
                joined_at=user_model.joined_at,
                is_active=user_model.is_active,
                hashed_password=user_model.hashed_password,
                refresh_token=user_model.refresh_token,
                role=user_model.role
            )
    
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        async with self.async_session as session:
            query = select(UserModel).where(UserModel.email == email, UserModel.is_active == True)
            query_result = await session.execute(query)
            user_model = query_result.scalar_one_or_none()
            if not user_model:
                return None
            return UserEntity(
                id=user_model.id,
                full_name=user_model.full_name,
                phone_number=user_model.phone_number,
                email=user_model.email,
                address=user_model.address,
                updated_at=user_model.updated_at,
                joined_at=user_model.joined_at,
                is_active=user_model.is_active,
                hashed_password=user_model.hashed_password,
                refresh_token=user_model.refresh_token,
                role=user_model.role
            )
    
    async def delete_by_id(self, id: int) -> bool:
        async with self.async_session as session:
            query = (
                update(UserModel)
                .where(UserModel.id == id)
                .values(is_active=False)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
    
    async def delete_by_email(self, email: str) -> bool:
        async with self.async_session as session:
            query = (
                update(UserModel)
                .where(UserModel.email == email)
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
                id=user_model.id,
                full_name=user_model.full_name,
                phone_number=user_model.phone_number,
                email=user_model.email,
                address=user_model.address,
                updated_at=user_model.updated_at,
                joined_at=user_model.joined_at,
                is_active=user_model.is_active,
                hashed_password=user_model.hashed_password,
                refresh_token=user_model.refresh_token,
                role=user_model.role
            )
    
    async def update(self, user_entity: UserEntity) -> UserEntity:
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
                    )
                    .returning(UserModel)
                )
                result = await session.execute(query)
                user_model = result.scalar_one()
            return UserEntity(
                id=user_model.id,
                full_name=user_model.full_name,
                phone_number=user_model.phone_number,
                email=user_model.email,
                address=user_model.address,
                updated_at=user_model.updated_at,
                joined_at=user_model.joined_at,
                is_active=user_model.is_active,
                hashed_password=user_model.hashed_password,
                refresh_token=user_model.refresh_token,
                role=user_model.role
            )