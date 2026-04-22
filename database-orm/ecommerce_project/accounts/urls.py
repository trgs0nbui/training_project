from django.urls import path, include
from .views import register_api, login_api, logout_view, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('api/register', register_api, name='register'),
    path('api/login', login_api, name='login'),
    path('api/logout', logout_view, name='logout'),
    path('api/', include(router.urls))
]