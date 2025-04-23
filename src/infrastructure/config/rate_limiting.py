from slowapi import Limiter
from slowapi.util import get_remote_address

from .variables import REDIS_URL

limiter = Limiter(key_func=get_remote_address, storage_uri=REDIS_URL)
