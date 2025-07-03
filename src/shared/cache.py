import json
from typing import Any

import redis
import redis.asyncio

from src.config import settings


class CacheService:
    def __init__(self, connection_url: str = settings.cache.redis_url) -> None:
        self.connection = redis.asyncio.from_url(connection_url)

    def _build_key(self, namespace: str, key: Any) -> str:
        return f"{namespace}:{key}"

    async def save(
        self,
        namespace: str,
        key: Any,
        instance: dict,
        ttl: int | None = None,
    ) -> None:
        payload = json.dumps(instance)

        await self.connection.set(
            self._build_key(namespace, key), payload, ex=ttl
        )  # noqa: E501

    async def get(self, namespace: str, key: Any) -> dict | None:
        result = await self.connection.get(self._build_key(namespace, key))
        if not result:
            return None
        return json.loads(result)  # type: ignore

    async def delete(self, activation_token):
        await self.connection.delete(
            self._build_key("activation", activation_token)
        )  # noqa: E501
