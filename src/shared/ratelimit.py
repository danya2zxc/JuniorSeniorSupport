import redis
import redis.asyncio
from fastapi import HTTPException, status

from src.config import settings


class RateLimitService:
    def __init__(self):
        self.client = redis.asyncio.from_url(settings.cache.redis_url)

    async def increment_and_check_limit(self, key: str, limit: int, ttl: int):
        current = await self.client.incr(key)
        if current == 1:
            await self.client.expire(key, ttl)
        if current > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded, try again later.",
            )
