import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_register_api(api_client):
    # Kiểm tra behavior: Gọi API đăng ký tạo thành công user trả về mã status 201
    url = reverse('register')
    response = api_client.post(url, {
        "username": "apiuser",
        "email": "api@gmail.com",
        "password": "12345678",
        "confirm_password": "12345678"
    }, format="json")

    assert response.status_code == 201
    assert response.data["success"] is True
    assert "access" in response.data

@pytest.mark.django_db
def test_login_api(api_client):
    # Kiểm tra behavior: Đăng nhập với credentials đúng trả về mã 200 OK và access token
    User.objects.create_user(username="apiuser", password="12345678")
    url = reverse('login')
    response = api_client.post(url, {
        "username": "apiuser",
        "password": "12345678"
    }, format="json")

    assert response.status_code == 200
    assert response.data["success"] is True
    assert "access" in response.data

@pytest.mark.django_db
def test_login_fail_invalid_credentials_api(api_client):
    # Kiểm tra behavior: Đăng nhập sai user thì throw lỗi 401 UNAUTHORIZED
    url = reverse('login')
    response = api_client.post(url, {
        "username": "incorrectuser",
        "password": "12345678"
    }, format="json")

    assert response.status_code == 401
    assert response.data["success"] is False
    assert response.data["message"] == "Invalid credentials"

@pytest.mark.django_db
def test_user_list_api_protected(api_client):
    # Kiểm tra behavior: GET user endpoint không cần login (IsAuthenticatedOrReadOnly)
    url = reverse('user-list')
    response = api_client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_user_endpoint_auth(api_client):
    # Kiểm tra behavior: POST tạo endpoint theo quyền readonly trên views cần phải truyền Auth (IsAuthenticatedOrReadOnly)
    url = reverse('user-list')
    response = api_client.post(url, {
        "username": "newuser",
        "password": "12345678"
    }, format="json")

    assert response.status_code == 401
