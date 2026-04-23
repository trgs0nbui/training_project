from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from accounts.services.email_service import EmailService

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
            "user": user
        }

    @staticmethod
    def register(data):
        password = data.pop("password")
        confirm_password = data.pop("confirm_password")

        if password != confirm_password:
            raise AuthenticationFailed("Passwords do not match")

        if User.objects.filter(username=data.get("username")).exists():
            raise AuthenticationFailed("Username already exists")

        user = User.objects.create_user(password=password, **data)

        # Trigger async email task
        EmailService.send_welcome_email(user)
        
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }