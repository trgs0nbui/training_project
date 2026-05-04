from django.core.cache import cache
import json
from typing import Optional, Dict, Any

class RedisCache:
    """
        Wrapper for Redis cache operations with JSON serialization
    """
    
    USER_CACHE_TTL = 3600
    USER_CACHE_KEY = "user:{user_id}"
    USERS_LIST_CACHE_KEY = "user:all"
    
    @staticmethod
    def cache_user(user_id: int, user_data: Dict[str, Any]) -> None:
        """
            Cache user data in Redis
            Args:
                user_id: User ID
                user_data: Dictionary containing user data
        """
        cache_key = RedisCache.USER_CACHE_KEY.format(user_id = user_id)
        cache.set(cache_key, user_data, timeout=RedisCache.USER_CACHE_TTL)
        
    
    @staticmethod
    def get_cached_user(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached user data from Redis
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary containing user data or None if not found
        """
        
        cache_key = RedisCache.USER_CACHE_KEY.format(user_id=user_id)
        cache.delete(cache_key)
        
    @staticmethod
    def invalidate_all_users_cache() -> None:
        """
        Remove all users list from cache
        """
        cache.delete(RedisCache.USERS_LIST_CACHE_KEY)