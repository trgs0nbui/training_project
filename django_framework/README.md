# Report về cấu trúc folder của project Django (các folder/file chính)

## Sơ đồ cấu trúc thư mục đảm bảo cho việc scalable và deploy

```
myproject/
│
├── manage.py
├── .env
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── config/                  # Thư mục project chính
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   │
│   └── settings/            # Tách settings theo môi trường
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/                    # Chứa các app
│   ├── users/
|   |   |__ migrations/
|   |   |__ admin.py
|   |   |__ apps.py
|   |   |__ models.py
|   |   |__ views.py
|   |   |__ urls.py
|   |   |__ tests.py
|   |
│   ├── products/
│   └── orders/
│
├── core/                    # Logic dùng chung
│   ├── __init__.py
│   ├── models.py
│   ├── permissions.py
│   ├── services.py
│   └── utils.py
│
├── templates/
├── static/
├── media/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── scripts/                 # Script deploy / automation
│   └── entrypoint.sh
│
├── nginx/                   # Config web server
│   └── nginx.conf
│
└── logs/
```

## Nhiệm vụ chi tiết từng folder và file
---
### `manage.py`
- File chứa dòng lệnh để quản lý project, dùng để chạy server, migrate database
---
### Folder `migrations/`
- Lưu lịch sử thay đổi database
---
### `admin.py`
- File đảm nhận việc đăng ký model để quản lý bên trong app
---
### `apps.py`
- File cấu hình thông tin app, Django nhận diện app thông qua file này
---
### `models.py`
- File định nghĩa database schema bằng python class
---
### `views.py`
- File xử lý logic nghiệp vụ của app
---
### `tests.py`
- Fild viết test cho app
### `.env`
- Lưu các biến môi trường (chỉ lưu ở local, đảm bảo bảo mật đối với file này)
---
### Folder `requirements/`
- Đảm nhận việc quản lý các dependencies, tách biệt từng nhiệm vụ riêng cho từng file 
    - Ví dụ: base.txt quản lý các thư viện chung, prod.txt quản lý các thư viện riêng biệt ví dụ như database, 
        dev.txt quản lý thư viện phục vụ dev, test
---
### Folder `config`
#### Folder `settings/`
- base.py: Đảm nhận cấu hình chung về middleware, templates,...
- dev.py: Đảm nhận cấu hình cho môi trường development
- prod.py: Đảm nhận cấu hình cho môi trường production
- urls.py: là route tổng của project
- wsgi.py và asgi.py: Là cầu nối để kết nối web server trong khi deploy lên production server
- __init__.py: Vai trò của file này là đánh dấu folder như một Python 

---
## Folder `apps/`
- Chứa các app của project Django, đảm bảo tách biệt các logic đối với từng module trong 1 hệ thống

---
## Folder `core/`
- Chứa các logic dùng chung cho toàn hệ thống tránh việc code lặp lại trong hệ thống
    - Ví dụ: + services.py: chứa logic dùng chung về nghiệp vụ hệ thống
             + ultils.py: chứa các function hoặc class dùng xuyên suốt trong 1 project
             + permissions.py: chứa logic cho việc phần quyền

---
## Folder `templates/`
- Chứa file HTML của hệ thống (UI)
---
## Folder `static/`
- Chứa các file tĩnh như CSS, JS 
---
## Folder `media/`
- Chứa các file upload ví dụ như avatar, ...
---
## Folder `docker/`
- Chứa các file Dockerfile, yml phục vụ việc đóng gói các dịch vụ hiện có trong hệ thống: PostgreSQL, Django, Redis...
---
## Folder `scripts/`
- Chứa file .sh phục vụ cho việc migrate, run server, ...
---
## Folder `nginx/`
- Có thể được sử dụng khi cần mở rộng hệ thống về load balancing, ...
---
## Folder `logs/`
- Nhiệm vụ của folder này là để lưu lại log của production, debug lỗi server
