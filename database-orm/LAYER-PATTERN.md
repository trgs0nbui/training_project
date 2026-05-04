# SERVICE LAYER & REPOSITORY PATTERN
---
## SERVICE LAYER

### Service layer là gì?
- Service layer là 1 pattern hướng kiến trúc xác định tập các dịch vụ để xử lý các logic nghiệp vụ và hành động tức thì giữa các lớp khác nhau của 1 ứng dụng,
đặc biệt là Controller và Repository 

### Vì sao nên sử dụng Service Layer
1. Tách biệt các mối quan tâm: Bằng cách tách biệt các logic nghiệp vụ trong service layer, ta có thể giữ code độc lập và tách rời nhau,
Điều này giúp các lớp của ứng dụng tập trung vào 1 nhiệm vụ duy Nhất

2. Có thể sử dụng lại code: Service layer cho phép ta dùng lại các logic nghiệp vụ giữa các phần khác nhau của ứng dụng. Thay vì lặp lại đoạn code đó nhiều lần và ở nhiều nơi,
ta tập trung xây dựng logic ở services nơi mà có thể truy cập từ bất cứ đâu trong ứng dụng

3. Bảo trì được
4. Kiểm thử được

### Đặc điểm chính của Service Layer
1. Tập trung logic nghiệp vụ: Mục tiêu chính của 1 service layer là đóng gói toàn bộ các logic và rule nghiệp vụ
2. Quản lý Transaction: Trong nhiều ứng dụng, services xử lý các đường biên giao dịch, đảm bảo tính ổn định và khả năng rollback giữa những nền tảng cơ sở dữ liệu
3. Xử lý tích hợp: Service Layer chịu trách nhiệm tích hợp với những hệ thống và ứng dụng khác như API của bên thứ ba, Redis, ...

### Nên sử dụng Service Layer khi nào
1. SL được sử dụng khi ta có logic nghiệp vụ phức tạp mà cần tách riêng từ web hay lớp truy cập dữ liệu
2. Khi ứng dụng cần tích hợp những hệ thống bên ngoài
3. Khi cần 1 hệ thống rõ ràng và cần khả năng kiểm thử độc lập giữa hàng loạt các layer của ứng dụng.


## SERVICE LAYER & REPOSITORY PATTERN TRONG DJANGO

Trong quá trình phát triển ứng dụng Django, việc tổ chức code hợp lý
giúp: - Dễ bảo trì - Dễ test - Dễ mở rộng

Ba khái niệm quan trọng: - Service Layer - Repository Pattern - Phân
biệt Fat Models vs Thin Models

---

### 1. Service Layer là gì?

Service Layer là tầng chứa business logic của ứng dụng.

#### Vai trò:

-   Xử lý logic nghiệp vụ
-   Không phụ thuộc vào HTTP (request/response)
-   Có thể tái sử dụng

#### Ví dụ KHÔNG tốt (logic trong views):

``` python
# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Order

def create_order(request):
    user = request.user
    total = 0

    for item in request.POST.get('items'):
        total += item['price'] * item['quantity']

    order = Order.objects.create(user=user, total=total)
    
    return JsonResponse({'id': order.id})
```

#### Vấn đề:

-   View phình to
-   Khó test
-   Không tái sử dụng được

#### Ví dụ TỐT (dùng Service Layer):

``` python
# services/order_service.py
from .models import Order

def create_order(user, items):
    total = sum(item['price'] * item['quantity'] for item in items)
    return Order.objects.create(user=user, total=total)
```

``` python
# views.py
from django.http import JsonResponse
from .services.order_service import create_order

def create_order_view(request):
    order = create_order(request.user, request.POST.get('items'))
    return JsonResponse({'id': order.id})
```

---
## 3. Repository Pattern là gì?

Repository Pattern giúp tách việc truy cập database ra khỏi logic nghiệp vụ.

### Vai trò:

-   Đóng gói ORM query
-   Chịu trách nhiệm cho các thao tác CRUD cơ bản với DB, và là lớp duy nhất giao tiếp trực tiếp với DB
-   Dễ mock data khi test

### Ví dụ KHÔNG tốt:

``` python
# services/order_service.py
from .models import Order

def get_user_orders(user):
    return Order.objects.filter(user=user, status='completed')
```

### Ví dụ TỐT:

``` python
# repositories/order_repository.py
from .models import Order

class OrderRepository:
    @staticmethod
    def get_completed_orders_by_user(user):
        return Order.objects.filter(user=user, status='completed')
```

``` python
# services/order_service.py
from .repositories.order_repository import OrderRepository

def get_user_orders(user):
    return OrderRepository.get_completed_orders_by_user(user)
```

---

## 4. Fat Models vs Thin Models vs Service Layer

### 4.1 Fat Models

Đưa toàn bộ business logic vào models

``` python
# models.py
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()

    def calculate_total(self, items):
        return sum(item['price'] * item['quantity'] for item in items)
```

#### Ưu điểm:

-   Logic gần dữ liệu

#### Nhược điểm:

-   Model trở nên phức tạp
-   Khó reuse
-   Khó test

---

### 4.2 Thin Models

Model chỉ giữ dữ liệu

``` python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
```

#### Ưu điểm:

-   Đơn giản, dễ kiểm soát các trường của model

#### Nhược điểm:

-   Logic bị dồn sang views

---

### 4.3 Service Layer

``` python
# services/order_service.py
def calculate_total(items):
    return sum(item['price'] * item['quantity'] for item in items)
```

#### Ưu điểm:

-   Tách biệt rõ ràng
-   Dễ test
-   Dễ mở rộng

---

## 5. Tại sao nên tách business logic khỏi views?

### 5.1 Vấn đề khi để trong views:

-   View trở nên khó đọc
-   Không thể reuse
-   Khó unit test

### 5.2 Lợi ích khi tách ra:

#### 1. Dễ test

``` python
def test_calculate_total():
    items = [{'price': 10, 'quantity': 2}]
    assert calculate_total(items) == 20
```

#### 2. Tái sử dụng

-   Dùng cho API
-   Dùng cho Celery task
-   Dùng cho CLI script

#### 3. Clean Architecture

-   View: chỉ xử lý HTTP
-   Service: xử lý business
-   Repository: xử lý DB

---

## 6. Kết luận

-   Service Layer giúp tách business logic khỏi views, giúp views tập trung vào nhiệm vụ nhận request từ service và trả response
-   Repository Pattern giúp tách database access
-   Tránh Fat Models và Thin Models cực đoan
-   Nên kết hợp:
    -   Models: dữ liệu
    -   Repository: truy vấn db
    -   Service: logic nghiệp vụ
    -   View: HTTP handling
