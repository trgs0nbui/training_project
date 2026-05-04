import pytest
from django.urls import reverse
from shop.models import Category, Product
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_product_api_list(api_client):
    # Kiểm tra behavior: Endpoint GET public lấy danh sách products trả về 200 HTTP OK
    category = Category.objects.create(name="Device")
    Product.objects.create(name="Phone", price=400.00, category=category, description="D")
    
    url = reverse('product-list')
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data["success"] is True
    assert "data" in response.data

@pytest.mark.django_db
def test_product_api_create_unauthorized(api_client):
    # Kiểm tra behavior của Permission IsAuthenticatedOrReadOnly: Cần POST header auth để ghi dữ liệu
    url = reverse('product-list')
    
    # Gửi requests không có thông tin auth
    response = api_client.post(url, {
        "name": "New Phone",
        "price": 500,
        "description": "demo"
    }, format="json")
    
    # Nên trả về lỗi 401
    assert response.status_code == 401

@pytest.mark.django_db
def test_product_validation_error(api_client):
    # Kiểm tra trường hợp price <= 0 trả về Validation Error trên API từ Exception do Custom trong viewset handle
    
    # Bypass logic IsAuthenticated
    user = User.objects.create_user(username="admin", password="123")
    api_client.force_authenticate(user=user)
    
    category = Category.objects.create(name="Tech")
    
    url = reverse('product-list')
    response = api_client.post(url, {
        "name": "Free item",
        "price": 0, # Trigger logic kiểm tra giá sản phẩm
        "category": category.id,
        "description": "demo text content"
    }, format="json")
    
    # 400 Bad request trả về từ validation lỗi serialize field
    assert response.status_code == 400
    assert "price" in response.data
    assert "Giá sản phẩm phải lớn hơn 0" in str(response.data["price"])
