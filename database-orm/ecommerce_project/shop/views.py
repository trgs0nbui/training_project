from django.shortcuts import render
from .models import *
from django.db.models import Count, Sum, F

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
    