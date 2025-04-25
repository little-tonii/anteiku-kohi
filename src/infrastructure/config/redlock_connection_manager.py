from typing import List
from .variables import (
    REDLOCK_URL_1,
    REDLOCK_URL_2,
    REDLOCK_URL_3
)
from redis.asyncio import Redis

REDLOCK_CONNECTIONS_URL = [
    REDLOCK_URL_1,
    REDLOCK_URL_2,
    REDLOCK_URL_3
]

redlock_connection_manager: List[Redis] = [
    Redis.from_url(
        redlock_url,
        decode_responses=False,
        socket_connect_timeout=5
    )
    for redlock_url in REDLOCK_CONNECTIONS_URL
]
