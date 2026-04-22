# ⚡ Quick Start - Docker + Django

## 🚀 Bắt Đầu Nhanh (5 phút)

### Bước 1: Tạo .env file

```bash
cp .env.example .env
```

Cập nhật các giá trị quan trọng:

```env
SECRET_KEY=your-generated-key-here
POSTGRES_PASSWORD=your-strong-password
```

**Tạo SECRET_KEY an toàn:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Bước 2: Build & Run

```bash
# Build Docker images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Bước 3: Setup Database

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Bước 4: Access Ứng Dụng

- **Admin**: http://localhost/admin
- **API**: http://localhost/api
- **Health Check**: http://localhost/health

---

## 📋 Các Lệnh Thường Dùng

```bash
# Logs
docker-compose logs -f web          # Django logs
docker-compose logs -f db           # Database logs
docker-compose logs -f nginx        # Nginx logs

# Database
docker-compose exec web python manage.py shell
docker-compose exec db psql -U ecommerce_user -d ecommerce

# Migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Restart
docker-compose restart

# Stop
docker-compose stop

# Clean up
docker-compose down
docker-compose down -v  # Remove volumes (DELETE DATABASE!)
```

---

## 🔧 Troubleshooting Nhanh

| Vấn đề                  | Giải pháp                                                          |
| ----------------------- | ------------------------------------------------------------------ |
| Port đang sử dụng       | `lsof -i :8000` và kill process                                    |
| Database không kết nối  | Restart: `docker-compose restart db`                               |
| Static files không load | `docker-compose exec web python manage.py collectstatic --noinput` |
| Permission error        | Xóa container và volume: `docker-compose down -v`                  |

---

## 📝 Environment Variables

```env
# Security (THAY ĐỔI NGAY)
DEBUG=False                          # Set False in production
SECRET_KEY=your-secret-key-here     # Generate using Django

# Database
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=strong-password   # Min 20 chars

# Hosts
ALLOWED_HOSTS=localhost,yourdomain.com
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://yourdomain.com

# CORS (nếu frontend riêng)
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Ports
DB_PORT=5432
WEB_PORT=8000
```

---

## 📚 Tài Liệu Chi Tiết

- [DOCKER-SETUP.md](DOCKER-SETUP.md) - Complete guide
- [SECURITY-BEST-PRACTICES.md](SECURITY-BEST-PRACTICES.md) - Security details
- [requirements.txt](requirements.txt) - Dependencies

---

## ❓ FAQ

**Q: Tại sao cần thiết lập .env?**  
A: Để che giấu thông tin nhạy cảm (passwords, API keys, secret keys) không được commit vào git.

**Q: Có cách nào ngăn chặn commit .env?**  
A: Có, đã thêm vào .gitignore rồi. Kiểm tra:

```bash
cat .gitignore | grep ".env"
```

**Q: Production dùng gì thay vì .env?**  
A: Dùng Docker Secrets, AWS Secrets Manager, hoặc HashiCorp Vault.

**Q: Làm sao backup database?**  
A:

```bash
docker-compose exec db pg_dump -U ecommerce_user ecommerce > backup.sql
```

**Q: Muốn scale application?**  
A: Dùng multiple web containers:

```yaml
web:
    deploy:
        replicas: 3
```

---

**Version**: 1.0 | Last Updated: 2026-04-22
