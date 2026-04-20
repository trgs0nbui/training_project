from django.urls import path
from .views import create_product, update_product,product_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
    path('update/<int:id>/', update_product, name ='update_product')
]