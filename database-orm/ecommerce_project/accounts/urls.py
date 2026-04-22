from django.urls import path, include
from .views import LoginAPIView, RegisterAPIView, LogoutAPIView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('api/register', RegisterAPIView.as_view(), name='register'),
    path('api/login', LoginAPIView.as_view(), name='login'),
    path('api/logout', LogoutAPIView.as_view(), name='logout'),
    path('api/', include(router.urls))
]