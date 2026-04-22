import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from accounts.services.auth_service import AuthService
from accounts.services.user_service import UserService

@pytest.mark.django_db
def test_register_success():
    # Kiểm tra behavior: Đăng ký thành công với thông tin hợp lệ
    # Action: gọi service tạo user
    result = AuthService.register({
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "12345678",
        "confirm_password": "12345678"
    })

    # Cần đảm bảo có trả về user và cặp token access/refresh
    assert result["user"].username == "testuser"
    assert "access" in result
    assert "refresh" in result
    
    # Đảm bảo database đã ghi nhận user mới thay đổi sau transaction (sẽ được tự động rollback)
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_register_password_mismatch():
    # Kiểm tra behavior: Đăng ký thất bại khi password và confirm_password khác nhau
    with pytest.raises(AuthenticationFailed) as excinfo:
        AuthService.register({
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "12345678",
            "confirm_password": "wrongpassword"
        })
    
    assert str(excinfo.value) == "Passwords do not match"
    
    # Đảm bảo record không bao giờ được tạo trong database
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_login_success():
    # Kiểm tra behavior: Đăng nhập thành công trả về access và refresh token
    user = User.objects.create_user(username="testuser", password="12345678")
    
    result = AuthService.login({
        "username": "testuser",
        "password": "12345678"
    })

    assert "access" in result
    assert "refresh" in result
    assert result["user"] == user

@pytest.mark.django_db
def test_login_invalid_credentials():
    # Kiểm tra behavior: Fail do mật khẩu không đúng sẽ throw lỗi AuthenticationFailed
    User.objects.create_user(username="testuser", password="12345678")
    
    with pytest.raises(AuthenticationFailed) as excinfo:
        AuthService.login({
            "username": "testuser",
            "password": "wrongpassword"
        })
    
    assert str(excinfo.value) == "Invalid credentials"

@pytest.mark.django_db
def test_login_inactive_user():
    # Kiểm tra behavior: Fail do user không còn is_active
    User.objects.create_user(username="testuser", password="12345678", is_active=False)
    
    with pytest.raises(AuthenticationFailed) as excinfo:
        AuthService.login({
            "username": "testuser",
            "password": "12345678"
        })
    
    assert "User is inactive" in str(excinfo.value)
