from abc import abstractmethod
from abc import ABC
from typing import Optional
from ..entity.reset_password_code_entity import ResetPasswordCodeEntity

class ResetPasswordCodeRepository(ABC):
    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, user_id: int, code: str) -> ResetPasswordCodeEntity:
        pass

    @abstractmethod
    async def find_by_code_and_user_id(self, code: str, user_id: int) -> Optional[ResetPasswordCodeEntity]:
        pass
