from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Count, Sum, F
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from rest_framework import viewsets, permissions, filters
from .serializers import ProductSerializer, ProductCreateSerializer
from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.response import Response

# QuerySet với filter và select_related
def product_list(request):
    min_price = request.GET.get('min_price', 0)
    
    products = Product.objects.filter(
        price__gte = min_price
    ).select_related('category') # Lọc ra những sản phẩm có giá >= min_price có category
    
    return render(request, 'shop/product_list.html', {
        'products': products
    })
    
# QuerySet với Filter và Prefetch_related
def product_by_tag(request, tag_name):
    products = Product.objects.filter(
        tags__name = tag_name
    ).prefetch_related('tags') # Lọc ra những sản phẩm theo tag và hiển thị tag của từng sản phẩm
    
    return render(request, 'shop/product_list.html', {
        'products': products
    })
    
# QuerySet với prefetch_related và annotate
@login_required
def order_list(request):
    orders = Order.objects.select_related('user').prefetch_related(
        'items__product'
    ).annotate(
        total=Sum(F('items__price') * F('items__quantity'))
    ) # Hiển thị những orders của user có item và sản phẩm sau đó tính tổng tiền orders
    
    return render(request, 'shop/order_list.html', {
        'orders': orders
    })
    
# QuerySet sử dụng aggregate
def dashboard(request):
    total_products = Product.objects.count()
    
    revenue = OrderItem.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    ) # Trả về tổng số doanh thu 
    
    return render(request, 'shop/dahshboard.html', {
        'total_products': total_products,
        'revenue': revenue['total']
    })

@login_required
def product_list(request):
    products = Product.objects.select_related(
        'category'
    ).prefetch_related(
        'tags', 'images'
    )

    return render(request, 'shop/product_list.html', {
        'products': products
    })

##########
@permission_required('shop.add_product', raise_exception=True)
def create_product(request):
    form = ProductForm()
    
    if request.method == "POST":
        form = ProductForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('product_list')
        
    return render(request, 'shop/product_form.html', {
        'form': form
    })
    
@permission_required('shop.change_product', raise_exception=True)
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    form = ProductForm(instance=product)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():
            form.save()
            return redirect('product_list')
        
    return render(request, 'shop/product_form.html', {
        'form': form
    })
    
@permission_required('shop.delete_product', raise_exception=True)
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product is deleted')
        
        return redirect('product_list')
    
    return render(request, 'shop/product_list.html', {
        'products': product
    })
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Định nghĩa filter sẽ sử dụng
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'tags']
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name', 'price']
    ordering = ['id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        
        return ProductSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        data = serializer.data
        if page is not None:
            return self.get_paginated_response({
                "success": True,
                "message": "Lấy danh sách sản phẩm thành công.",
                "data": data
            })
        return Response({
            "success": True,
            "message": "Lấy danh sách sản phẩm thành công.",
            "data": data
        })

    def retrieve(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        serializer = self.get_serializer(product)
        return Response({
            "success": True,
            "message": "Lấy chi tiết sản phẩm thành công.",
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "success": True,
            "message": "Tạo sản phẩm thành công.",
            "data": response.data
        }
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "success": True,
            "message": "Cập nhật sản phẩm thành công.",
            "data": response.data
        }
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Xóa sản phẩm thành công.",
            "data": None
        })

    def perform_create(self, serializer):
        price = serializer.validated_data.get('price', 0)
        if price <= 0:
            raise ValidationError({"price": "Giá sản phẩm phải lớn hơn 0."})
        serializer.save()