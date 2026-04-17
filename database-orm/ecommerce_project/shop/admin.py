from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name',)
    list_filter = ('category', )
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    
admin.site.register(Profile)
admin.site.register(ProductImage)
admin.site.register(OrderItem)