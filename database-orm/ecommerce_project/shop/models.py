from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# One To One with User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children'
                            )
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='products', blank=True)
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    
    def __str__(self):
        return f"Image of {self.product.name}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    
    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail')
    weight = models.FloatField()
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Detail of {self.product.name}"
    
"""
    User - Profile: One To One
    Product - Category: Many To One
    User - Order: One To Many
    Product - Order: Many To Many (represented by OrderItem)
"""