import json
from typing import Any

import redis

from src.config import settings


class CacheService:
    def __init__(self, connection_url: str = settings.cache.redis_url) -> None:
        self.connection = redis.Redis.from_url(connection_url)

    def _build_key(self, namespace: str, key: Any) -> str:
        return f"{namespace}:{key}"

    def save(
        self,
        namespace: str,
        key: Any,
        instance: dict,
        ttl: int | None = None,
    ) -> None:
        payload = json.dumps(instance)

        self.connection.set(self._build_key(namespace, key), payload, ex=ttl)

    def get(self, namespace: str, key: Any) -> dict | None:
        result = self.connection.get(self._build_key(namespace, key))
        if not result:
            return None
        return json.loads(result)  # type: ignore

    def delete(self, activation_token):
        self.connection.delete(self._build_key("activation", activation_token))
