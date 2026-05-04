from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from accounts.services.email_service import EmailService
from accounts.cache.redis_client import RedisCache
import logging

logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def login(data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise AuthenticationFailed("Username and password are required")

        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }

    @staticmethod
    def register(data):
        """
        Register new user with Redis caching and async email task.

        Flow:
        1. Validate and create user in DB
        2. Generate JWT tokens
        3. Cache user in Redis
        4. Queue Celery task for welcome email (non-blocking)
        5. Return response immediately

        Args:
            data: Dictionary with username, email, password, confirm_password

        Returns:
            Dictionary with user data, access token, and refresh token
        """
        password = data.pop("password", None)
        confirm_password = data.pop("confirm_password", None)

        if password != confirm_password:
            raise AuthenticationFailed("Passwords do not match")

        if User.objects.filter(username=data.get("username")).exists():
            raise AuthenticationFailed("Username already exists")

        # 1. Create user in database
        user = User.objects.create_user(password=password, **data)
        logger.info(f"User created: {user.id} - {user.username}")

        # 2. Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        logger.info(f"JWT tokens generated for user {user.id}")

        # 3. Cache user in Redis (for faster subsequent lookups)
        user_cache_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
        }
        RedisCache.cache_user(user.id, user_cache_data)
        logger.info(f"User {user.id} cached in Redis")

        # 4. Queue Celery task for welcome email (async, non-blocking)
        task_id = EmailService.send_welcome_email(user)
        if task_id:
            logger.info(f"Email task queued with ID: {task_id}")

        # 5. Return response immediately (without waiting for email)
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "task_id": task_id,  # Optional: for tracking email task
        }

    @staticmethod
    def get_user_from_cache_or_db(user_id):
        """
        Get user from Redis cache, fall back to DB if not cached.

        Args:
            user_id: User ID

        Returns:
            User object
        """
        # 1. Try to get from Redis cache
        cached_user = RedisCache.get_cached_user(user_id)
        if cached_user:
            logger.info(f"User {user_id} retrieved from Redis cache")
            # Convert cache dict back to User object if needed
            return cached_user

        # 2. Fall back to database
        try:
            user = User.objects.get(id=user_id)
            # Cache it for next time
            user_cache_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "date_joined": (
                    user.date_joined.isoformat() if user.date_joined else None
                ),
            }
            RedisCache.cache_user(user.id, user_cache_data)
            logger.info(f"User {user_id} retrieved from DB and cached in Redis")
            return user
        except User.DoesNotExist:
            logger.warning(f"User {user_id} not found")
            raise AuthenticationFailed(f"User {user_id} not found")
