from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def health_check(request):
    """Health check endpoint for Docker"""
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("health", health_check, name="health_check"),
    path("auth/", include("accounts.urls")),
    path("shop/", include("shop.urls")),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
