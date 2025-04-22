from typing import Optional
from typing_extensions import override
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from .variables import REDIS_URL

redis = aioredis.from_url(
    url=REDIS_URL,
    encoding='utf-8',
    decode_responses=False,
)

REDIS_PREFIX = 'anteiku-kohi-cache'

class RedisNamespace:
    MEAL_LIST = "meal_list"
    MEAL = "meal"
    USER = "user"

class FastAPICacheExtended(FastAPICache):
    @classmethod
    @override
    async def clear(
        cls, namespace: Optional[str] = None, key: Optional[str] = None
    ) -> int:
        assert (  # noqa: S101
            cls._backend and cls._prefix is not None
        ), "You must call init first!"
        if namespace and namespace.strip() != "":
            namespace = cls._prefix + ":" + namespace
        return await cls._backend.clear(namespace, key)
