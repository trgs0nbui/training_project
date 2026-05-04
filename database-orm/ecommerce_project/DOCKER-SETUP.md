# 🐳 Django + PostgreSQL Docker Setup Guide

## 📋 Mục lục

1. [Cấu trúc file](#cấu-trúc-file)
2. [Thiết lập ban đầu](#thiết-lập-ban-đầu)
3. [Chạy ứng dụng](#chạy-ứng-dụng)
4. [Quản lý cơ sở dữ liệu](#quản-lý-cơ-sở-dữ-liệu)
5. [Lệnh hữu ích](#lệnh-hữu-ích)
6. [Biện pháp bảo mật](#biện-pháp-bảo-mật)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## 🗂️ Cấu trúc File

```
ecommerce_project/
├── Dockerfile                 # Multi-stage build image
├── docker-compose.yml         # Orchestration configuration
├── nginx.conf                # Reverse proxy config
├── .env.example              # Environment template
├── .dockerignore             # Docker build excludes
├── entrypoint.sh             # Startup script
├── requirements.txt          # Python dependencies
├── manage.py
├── ecommerce_project/
│   ├── settings.py          # 🔒 Updated with env variables
│   ├── urls.py
│   └── wsgi.py
├── accounts/
├── shop/
└── media/                    # Auto-created
```

---

## 🚀 Thiết lập Ban Đầu

### 1. Clone .env từ template

```bash
cp .env.example .env
```

### 2. Cấu hình biến môi trường

Chỉnh sửa `.env` với các giá trị thực:

```env
# Security - THAY ĐỔI CÁC GIÁ TRỊ NÀY
DEBUG=False
SECRET_KEY=generate-a-secure-key-using-django-command

# Database
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=your-strong-password-here  # Tối thiểu 20 ký tự

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 3. Tạo SECRET_KEY an toàn

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Sao chép output vào biến `SECRET_KEY` trong `.env`

### 4. Xây dựng Docker images

```bash
docker-compose build
```

---

## ▶️ Chạy Ứng Dụng

### Development Mode (Local)

```bash
docker-compose up -d
```

### Kiểm tra status

```bash
docker-compose ps

# Output:
# NAME                  STATUS
# ecommerce_db          Up
# ecommerce_web         Up
# ecommerce_nginx       Up
```

### Xem logs

```bash
# Tất cả services
docker-compose logs -f

# Chỉ Django
docker-compose logs -f web

# Chỉ PostgreSQL
docker-compose logs -f db

# Chỉ Nginx
docker-compose logs -f nginx
```

### Truy cập ứng dụng

- **API**: http://localhost (qua Nginx)
- **Direct**: http://localhost:8000 (Django)
- **Admin**: http://localhost/admin

---

## 🗄️ Quản lý Cơ Sở Dữ Liệu

### Chạy migrations

```bash
docker-compose exec web python manage.py migrate

# Hoặc tạo migration mới
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Tạo superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Backup Database

```bash
docker-compose exec db pg_dump -U ecommerce_user ecommerce > backup.sql

# Restore
docker-compose exec db psql -U ecommerce_user ecommerce < backup.sql
```

### Truy cập PostgreSQL Shell

```bash
docker-compose exec db psql -U ecommerce_user -d ecommerce

# Lệnh SQL hữu ích
\dt                    # Liệt kê các bảng
\l                     # Liệt kê các database
SELECT * FROM users;   # Query dữ liệu
```

### Reset Database (DANGER ⚠️)

```bash
# Xóa tất cả volumes (database bị mất!)
docker-compose down -v

# Xây dựng lại
docker-compose up -d
```

---

## 🛠️ Lệnh Hữu Ích

### Django Management

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check system
docker-compose exec web python manage.py check

# Shell Django
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Make fixtures
docker-compose exec web python manage.py dumpdata > data.json
```

### Docker Operations

```bash
# Rebuild images
docker-compose build --no-cache

# Restart containers
docker-compose restart

# Stop containers
docker-compose stop

# Remove containers & volumes
docker-compose down

# Remove images
docker rmi ecommerce_project-web
```

### Health Checks

```bash
# Check container health
docker-compose ps

# Inspect service
docker-compose exec web curl http://localhost:8000/health

# Check database connection
docker-compose exec web python -c "from django.db import connections; connections['default'].ensure_connection(); print('OK')"
```

---

## 🔒 Biện Pháp Bảo Mật

### ✅ Đã Triển Khai

#### 1. **Environment Variables**

- ✓ SECRET_KEY từ environment
- ✓ DEBUG=False trong production
- ✓ Database credentials được ẩn
- ✓ .gitignore để tránh commit .env

#### 2. **Non-root User**

- ✓ Django container chạy với user `django_user` (UID 1000)
- ✓ Database service chạy với user `postgres` (UID 999)

#### 3. **Security Headers** (trong settings.py)

```python
CSRF_COOKIE_SECURE = True      # HTTPS only
CSRF_COOKIE_HTTPONLY = True    # Không truy cập từ JS
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True     # Force HTTPS
X_FRAME_OPTIONS = 'DENY'       # Chống clickjacking
```

#### 4. **Network Isolation**

- ✓ Services kết nối qua `ecommerce_network` (internal)
- ✓ Chỉ port 80/443 (Nginx) mở ra ngoài

#### 5. **Database Security**

- ✓ Strong password requirement
- ✓ Non-default port option
- ✓ Health checks bảo vệ khỏi crashing

#### 6. **Nginx Reverse Proxy**

- ✓ SSL/TLS termination
- ✓ Gzip compression
- ✓ Rate limiting ready
- ✓ XSS protection headers

#### 7. **Container Hardening**

- ✓ `read_only_root_filesystem` cho critical services
- ✓ `cap_drop: ALL` - xóa tất cả capabilities
- ✓ `security_opt: no-new-privileges` - ngăn privilege escalation

#### 8. **Multi-stage Build**

- ✓ Giảm image size từ ~1.2GB → ~200MB
- ✓ Không chứa build tools trong production

### 📝 Checklist Trước Production

```bash
# 1. Thay đổi tất cả mật khẩu
# - DATABASE password
# - SECRET_KEY
# - Superuser password

# 2. Cấu hình SSL/TLS
# Uncomment SSL section trong nginx.conf
# Đặt cert.pem và key.pem trong ./ssl/

# 3. Cập nhật ALLOWED_HOSTS
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# 4. Kích hoạt HTTPS Redirect
# Uncomment trong nginx.conf HTTP block

# 5. Cấu hình Backup
# - Tạo cronjob cho pg_dump
# - Setup offsite backup

# 6. Monitoring
# - Setup logging
# - Configure alerting

# 7. Rate Limiting (Production)
# Thêm vào nginx.conf:
# limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
# limit_req zone=api burst=20 nodelay;
```

---

## 🚨 Troubleshooting

### Database Connection Error

```
ERROR: could not translate host name "db" to address

✓ Giải pháp:
- Đảm bảo db service đang chạy: docker-compose ps
- Kiểm tra network: docker network ls
- Restart: docker-compose restart db
```

### Port Already in Use

```
ERROR: bind: address already in use

✓ Giải pháp:
# Tìm process sử dụng port
lsof -i :8000
lsof -i :5432
lsof -i :80

# Kill process hoặc thay đổi port trong docker-compose.yml
```

### Static Files Not Loading

```
✓ Giải pháp:
docker-compose exec web python manage.py collectstatic --noinput
# Đảm bảo volume được mount đúng
# Kiểm tra nginx.conf location /static/
```

### Django Migrations Failed

```
✓ Giải pháp:
# Xem lỗi
docker-compose logs web

# Reset migrations (cẩn thận!)
docker-compose exec web python manage.py migrate --fake-initial

# Hoặc delete tất cả migrations và tạo lại
```

### Permission Denied Errors

```
✓ Giải pháp:
# Check file ownership
docker-compose exec web ls -la

# Fix permissions
docker-compose exec web chown -R django_user:django_user /app
```

### Memory Issues

```
✓ Giải pháp:
# Kiểm tra resource usage
docker stats

# Tăng Docker memory limit
# Settings → Resources → Memory
```

---

## 🌍 Production Deployment

### AWS EC2 Deployment

```bash
# 1. SSH vào EC2
ssh -i key.pem ubuntu@your-ec2-instance

# 2. Clone repository
git clone <repo-url>
cd ecommerce_project

# 3. Cài Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose

# 4. Setup .env
cp .env.example .env
# Cập nhật tất cả giá trị

# 5. Setup SSL Certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com

# 6. Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem
sudo chown $USER:$USER ./ssl/*

# 7. Build & Run
docker-compose build
docker-compose up -d

# 8. Auto-renew certificates
sudo systemctl enable certbot.timer
```

### Digital Ocean / Linode

```bash
# Tương tự AWS nhưng:
# - Sử dụng docker-compose file compatible
# - Setup firewall rules
# - Configure backups
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
    push:
        branches: [main]

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2

            - name: Build Docker image
              run: docker build -t myapp .

            - name: Push to Docker Hub
              run: docker push myapp:latest

            - name: Deploy to server
              run: |
                  ssh user@server 'cd app && docker-compose pull && docker-compose up -d'
```

---

## 📊 Monitoring & Logging

### Docker Logs

```bash
# Real-time logs
docker-compose logs -f

# Timestamp included
docker-compose logs -f --timestamps

# Follow chỉ errors
docker-compose logs web 2>&1 | grep ERROR
```

### Health Check Status

```bash
# View health status
docker-compose ps

# Manual health check
docker-compose exec web python manage.py check
docker-compose exec db pg_isready
```

### Resource Monitoring

```bash
# Real-time stats
docker stats

# Historical logs
docker inspect ecommerce_web | grep -A 10 State
```

---

## 🔄 Updates & Maintenance

### Update Dependencies

```bash
# Update Python packages
pip install -U -r requirements.txt
pip freeze > requirements.txt

# Rebuild image
docker-compose build --no-cache web
docker-compose up -d
```

### Database Migrations in Production

```bash
# Zero-downtime deployment
docker-compose exec web python manage.py migrate --plan

# Run migrations
docker-compose exec web python manage.py migrate

# Verify
docker-compose exec web python manage.py migrate --check
```

---

## 📚 Tài Nguyên Thêm

- [Docker Official Django](https://docs.docker.com/samples/django/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [PostgreSQL in Docker](https://hub.docker.com/_/postgres)
- [Nginx Best Practices](https://nginx.org/en/docs/)

---

**Last Updated**: 2026-04-22  
**Version**: 1.0
