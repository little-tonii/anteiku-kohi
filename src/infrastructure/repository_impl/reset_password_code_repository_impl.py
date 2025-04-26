from typing import Optional
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entity.reset_password_code_entity import ResetPasswordCodeEntity
from ..model.reset_password_code_model import ResetPasswordCodeModel
from ...domain.repository.reset_password_code_repository import ResetPasswordCodeRepository


class ResetPasswordCodeRepositoryImpl(ResetPasswordCodeRepository):
    async_session: AsyncSession

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def delete_by_user_id(self, user_id: int) -> bool:
        async with self.async_session as session:
            async with session.begin():
                stmt = (
                    delete(ResetPasswordCodeModel)
                    .where(
                        ResetPasswordCodeModel.user_id == user_id
                    )
                )
                result = await session.execute(stmt)
            if result.rowcount == 0:
                return False
        return True

    async def create(self, user_id: int, code: str) -> ResetPasswordCodeEntity:
        async with self.async_session as session:
            async with session.begin():
                reset_password_model = ResetPasswordCodeModel(user_id=user_id, code=code)
                stmt = insert(ResetPasswordCodeModel).values(
                    user_id=reset_password_model.user_id,
                    code=reset_password_model.code
                )
                await session.execute(stmt)
                await session.flush()
                await session.refresh(reset_password_model)
        return ResetPasswordCodeEntity(
            user_id=reset_password_model.user_id, # type: ignore
            code=reset_password_model.code, # type: ignore
            id=reset_password_model.id, # type: ignore
            created_at=reset_password_model.created_at, # type: ignore
        )

    async def find_by_code_and_user_id(self, code: str, user_id: int) -> Optional[ResetPasswordCodeEntity]:
        async with self.async_session as session:
            async with session.begin():
                stmt = (
                    select(ResetPasswordCodeModel)
                    .where(
                        ResetPasswordCodeModel.code == code,
                        ResetPasswordCodeModel.user_id == user_id
                    )
                )
                result = await session.execute(stmt)
                reset_password_model = result.scalar_one_or_none()
                if reset_password_model is None:
                    return None
        return ResetPasswordCodeEntity(
            user_id=reset_password_model.user_id, # type: ignore
            code=reset_password_model.code, # type: ignore
            id=reset_password_model.id, # type: ignore
            created_at=reset_password_model.created_at, # type: ignore
        )
