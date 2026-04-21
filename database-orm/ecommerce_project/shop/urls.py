from django.urls import path, include
from .views import create_product, update_product,product_list, ProductViewSet
# from .views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
    path('update/<int:id>/', update_product, name ='update_product'),
    path('api/', include(router.urls)),
]