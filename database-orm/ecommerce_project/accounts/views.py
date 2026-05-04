from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from accounts.services.auth_service import AuthService
from accounts.services.user_service import UserService
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.login(serializer.validated_data)
        except AuthenticationFailed as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "success": True,
            "access": result["access"],
            "refresh": result["refresh"]
        }, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.register(serializer.validated_data)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "access": result["access"],
            "refresh": result["refresh"]
        }, status=status.HTTP_201_CREATED)
        
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({
                    "success": False,
                    "message": "Refresh token is required"
                }, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "success": True,
                "message": "Logout successful"
            })

        except Exception:
            return Response({
                "success": False,
                "message": "Invalid token"
            }, status=400)
        
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['is_active', 'date_joined']
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username', 'date_joined']
    ordering = ['id']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin: 
            return UserService.list_users()
        return UserService.filter_users(id=user.id)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = UserService.get_user(kwargs['pk'])
        except Exception:
            raise NotFound("User can not be found")

        serializer = self.get_serializer(user)
        
        return Response({
            "success": True,
            "message": "Lấy chi tiết user thành công",
            "data": serializer.data
        })
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user(serializer.validated_data)
        output = self.get_serializer(user)
        return Response({
            "success": True,
            "message": "Tạo user thành công.",
            "data": output.data
        })

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.update_user(kwargs['pk'], serializer.validated_data)
        output = self.get_serializer(user)
        return Response({
            "success": True,
            "message": "Cập nhật user thành công.",
            "data": output.data
        })

    def destroy(self, request, *args, **kwargs):
        UserService.delete_user(kwargs['pk'])
        return Response({
            "success": True,
            "message": "Xóa user thành công.",
            "data": None
        })