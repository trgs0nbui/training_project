import pytest
from shop.models import Category, Product, Profile
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_profile_creation_isolation():
    # Kiểm tra isolation behavior của bảng Profile (Sẽ rollback sau chạy)
    user = User.objects.create_user(username="john_doe")
    profile = Profile.objects.create(user=user, address="123 ABC HT", phone="0987654321")
    
    assert profile.address == "123 ABC HT"
    assert str(profile) == "john_doe"

@pytest.mark.django_db
def test_category_relationship_isolation():
    # Kiểm tra behavior quan hệ parent-child của Category
    parent = Category.objects.create(name="Tech")
    child = Category.objects.create(name="Mobile", parent=parent)
    
    # Assert mối liên hệ FK được tạo ra thành công trước khi transaction rollback
    assert child.parent == parent
    assert parent.children.count() == 1
    assert parent.children.first() == child

@pytest.mark.django_db
def test_product_str():
    # Kiểm tra representation __str__ của object logic class Model
    category = Category.objects.create(name="Tech")
    product = Product.objects.create(name="Laptop Lenovo", price=1000.0, category=category, description="Demo desc")
    
    assert str(product) == "Laptop Lenovo"
