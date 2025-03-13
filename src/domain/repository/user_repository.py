from abc import ABC, abstractmethod
from typing import Optional
from ...domain.entity.user_entity import UserEntity


class UserRepository(ABC):
    
    @abstractmethod
    async def activate_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def activate_by_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    async def get_by_refresh_token(self, refresh_token: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def deactivate_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def deactivate_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def create(self, full_name: str, phone_number: str, email: str, address: str, hashed_password: str) -> UserEntity:
        pass
    
    @abstractmethod
    async def update(self, user_entity: UserEntity) -> UserEntity:
        pass