from typing import Optional

from sqlalchemy import delete, select, update
from domain.entity.staff_entity import StaffEntity
from domain.repository.staff_repository import StaffRepository
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.model.staff_model import StaffModel

class StaffRepositoryImpl(StaffRepository):
    async_session: AsyncSession
    
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
        
    async def get_by_id(self, id: int) -> Optional[StaffEntity]:
        async with self.async_session as session:
            query = select(StaffModel).where(StaffModel.id == id, StaffModel.is_active == True)
            query_result = await session.execute(query)
            staff_model = query_result.scalar_one_or_none()
            if not staff_model:
                return None
            return StaffEntity(
                id=staff_model.id,
                full_name=staff_model.full_name,
                phone_number=staff_model.phone_number,
                email=staff_model.email,
                address=staff_model.address,
                updated_at=staff_model.updated_at,
                joined_at=staff_model.joined_at,
                is_active=staff_model.is_active,
                hashed_password=staff_model.hashed_password,
                refresh_token=staff_model.refresh_token
            )
    
    async def get_by_email(self, email: str) -> Optional[StaffEntity]:
        async with self.async_session as session:
            query = select(StaffModel).where(StaffModel.email == email, StaffModel.is_active == True)
            query_result = await session.execute(query)
            staff_model = query_result.scalar_one_or_none()
            if not staff_model:
                return None
            return StaffEntity(
                id=staff_model.id,
                full_name=staff_model.full_name,
                phone_number=staff_model.phone_number,
                email=staff_model.email,
                address=staff_model.address,
                updated_at=staff_model.updated_at,
                joined_at=staff_model.joined_at,
                is_active=staff_model.is_active,
                hashed_password=staff_model.hashed_password,
                refresh_token=staff_model.refresh_token
            )
    
    async def delete_by_id(self, id: int) -> bool:
        async with self.async_session as session:
            query = (
                update(StaffModel)
                .where(StaffModel.id == id)
                .values(is_active=False)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
    
    async def delete_by_email(self, email: str) -> bool:
        async with self.async_session as session:
            query = (
                update(StaffModel)
                .where(StaffModel.email == email)
                .values(is_active=False)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def create(self, staff_entity: StaffEntity) -> StaffEntity:
        async with self.async_session as session:
            async with session.begin():
                staff_model = StaffModel(
                    full_name=staff_entity.full_name,
                    phone_number=staff_entity.phone_number,
                    email=staff_entity.email,
                    address=staff_entity.address,
                    hashed_password=staff_entity.hashed_password
                )
                session.add(staff_model)
                await session.flush()
            await session.refresh(staff_model)
            return StaffEntity(
                id=staff_model.id,
                full_name=staff_model.full_name,
                phone_number=staff_model.phone_number,
                email=staff_model.email,
                address=staff_model.address,
                updated_at=staff_model.updated_at,
                joined_at=staff_model.joined_at,
                is_active=staff_model.is_active,
                hashed_password=staff_model.hashed_password,
                refresh_token=staff_model.refresh_token
            )
    
    async def update(self, staff_entity: StaffEntity) -> StaffEntity:
        async with self.async_session as session:
            async with session.begin():
                query = (
                    update(StaffModel)
                    .where(StaffModel.id == staff_entity.id)
                    .values(
                        full_name=staff_entity.full_name,
                        phone_number=staff_entity.phone_number,
                        address=staff_entity.address,
                        hashed_password=staff_entity.hashed_password,
                        refresh_token=staff_entity.refresh_token,
                    )
                    .returning(StaffModel)
                )
                result = await session.execute(query)
                staff_model = result.scalar_one()
            return StaffEntity(
                id=staff_model.id,
                full_name=staff_model.full_name,
                phone_number=staff_model.phone_number,
                email=staff_model.email,
                address=staff_model.address,
                updated_at=staff_model.updated_at,
                joined_at=staff_model.joined_at,
                is_active=staff_model.is_active,
                hashed_password=staff_model.hashed_password,
                refresh_token=staff_model.refresh_token
            )