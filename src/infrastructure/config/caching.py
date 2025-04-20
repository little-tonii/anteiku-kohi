from redis import asyncio as aioredis

from .variables import REDIS_URL

redis = aioredis.from_url(
    url=REDIS_URL,
    encoding='utf-8',
    decode_responses=False,
)

class RedisNamespace:
    MEAL_LIST = "meal_list"
    MEAL = "meal"
