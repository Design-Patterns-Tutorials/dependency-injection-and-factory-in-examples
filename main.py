from abc import ABC, abstractmethod
from moke import Redis, Memcached
from enum import Enum


class ClientCacheBase(ABC):
    """Interface for Cache clients."""

    @abstractmethod
    def _set(self, key, value):
        """Caching Set: function used to set cache"""

    @abstractmethod
    def _get(self, key):
        """Caching Get: function used to get cache"""


class RedisClient(ClientCacheBase):
    def __init__(self, port, host, db):
        self.redis = Redis(port, host, db)

    def _set(self, key, value):
        self.redis.redis_set(key, value)

    def _get(self, key):
        return self.redis.redis_get(key)


class MemcachedClient(ClientCacheBase):
    def __init__(self, port, host):
        self.memcached = Memcached(port, host)

    def _set(self, key, value):
        self.memcached.memcached_set(key, value)

    def _get(self, key):
        return self.memcached.memcached_get(key)


class CacheService:
    def __init__(self, client: ClientCacheBase):
        self.client = client

    def set(self, key, value):
        self.client._set(key, value)

    def get(self, key):
        return self.client._get(key)


class CacheType(Enum):
    REDIS = 0
    MEMCACHED = 1


class CacheFactory:
    def getClient(self, cache_type: CacheType):
        if cache_type == CacheType.REDIS:
            redis_client = RedisClient(host="localhost", port=6379, db=0)
            return CacheService(client=redis_client)
        elif cache_type == CacheType.MEMCACHED:
            memcached_client = MemcachedClient(host="localhost", port=11211)
            return CacheService(client=memcached_client)


if __name__ == "__main__":
    cache_provider = CacheFactory()
    redis = cache_provider.getClient(CacheType.REDIS)
    memcached = cache_provider.getClient(CacheType.MEMCACHED)
    redis.set("username", "john_doe")
    username = redis.get("username")
    print(username)
    memcached.set("username", "john_doe2")
    username = memcached.get("username")
    print(username)