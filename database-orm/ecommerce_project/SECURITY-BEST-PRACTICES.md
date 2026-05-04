# 🔐 Docker + Django Security Best Practices

## 📋 Mục lục

1. [Secrets Management](#secrets-management)
2. [Container Security](#container-security)
3. [Network Security](#network-security)
4. [Application Security](#application-security)
5. [Database Security](#database-security)
6. [CI/CD Security](#cicd-security)
7. [Monitoring & Logging](#monitoring--logging)

---

## 🔑 Secrets Management

### ✅ DO - Đúng Cách

#### 1. Environment Variables (Hiện Tại)

```bash
# .env file (KHÔNG commit)
DEBUG=False
SECRET_KEY=your-super-secret-key
DB_PASSWORD=your-strong-password
```

```bash
# .gitignore
.env
.env.local
*.pem
*.key
```

#### 2. Docker Secrets (Production)

```yaml
# docker-compose.yml (Production)
services:
    db:
        environment:
            POSTGRES_PASSWORD_FILE: /run/secrets/db_password
        secrets:
            - db_password

secrets:
    db_password:
        file: ./secrets/db_password.txt
```

#### 3. AWS Secrets Manager / Vault

```python
# settings.py - Get secret from AWS
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

SECRET_KEY = get_secret('django/secret-key')
```

#### 4. HashiCorp Vault

```python
import hvac

client = hvac.Client(url='http://vault:8200')
secret = client.secrets.kv.read_secret_version(path='django')
SECRET_KEY = secret['data']['data']['secret_key']
```

### ❌ DON'T - Sai Cách

```python
# ❌ WRONG - Hardcoded secrets
SECRET_KEY = 'django-insecure-abc123xyz'
DATABASE_PASSWORD = 'password123'

# ❌ WRONG - Secrets trong environment variables (development)
# Không hash passwords, clear text

# ❌ WRONG - Commit .env file
git add .env  # NEVER!

# ❌ WRONG - Secrets trong docker-compose
environment:
  DB_PASSWORD: 'mypassword'  # Visible to everyone
```

---

## 🐳 Container Security

### ✅ Non-Root User

```dockerfile
# ✓ Correct
RUN useradd -m -u 1000 appuser
USER appuser

# ✗ Wrong
USER root
RUN apt-get install...
# Still running as root!
```

### ✅ Minimal Base Image

```dockerfile
# ✓ Use slim/alpine
FROM python:3.11-slim
FROM python:3.11-alpine

# ✗ Avoid
FROM ubuntu:22.04  # 77MB vs 350MB for slim
```

### ✅ Multi-Stage Build

```dockerfile
# ✓ Reduce image size and remove build artifacts
FROM python:3.11 as builder
RUN pip install -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /opt/venv /opt/venv
# Only includes runtime dependencies

# ✗ Single stage includes all build tools
```

### ✅ Security Options

```yaml
# docker-compose.yml
services:
    web:
        security_opt:
            - no-new-privileges:true # No privilege escalation
            - seccomp=default # Restrict syscalls
        cap_drop:
            - ALL
        cap_add:
            - NET_BIND_SERVICE # Only what's needed
        read_only_root_filesystem: true
        tmpfs:
            - /tmp
            - /run
```

### ❌ Security Anti-Patterns

```yaml
# ✗ NEVER DO THIS
services:
    web:
        privileged: true # Dangerous!
        user: root
        security_opt: []
        cap_add:
            - ALL
```

---

## 🌐 Network Security

### ✅ Network Isolation

```yaml
# docker-compose.yml
networks:
    internal:
        driver: bridge
        driver_opts:
            com.docker.network.bridge.default_bridge: "false"

services:
    web:
        networks:
            - internal
    db:
        networks:
            - internal
        # NOT exposed to host network
```

### ✅ Firewall Rules

```bash
# UFW (Ubuntu Firewall)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

### ✅ Port Exposure

```yaml
# ✓ Only expose necessary ports
services:
    nginx:
        ports:
            - "80:80"
            - "443:443"

    web:
        # NO ports exposed - only nginx
        networks:
            - internal

    db:
        # NO ports exposed - only internal network
        networks:
            - internal
```

### ❌ Security Issues

```yaml
# ✗ DON'T expose database to host
db:
    ports:
        - "5432:5432" # Anyone can access!

# ✗ DON'T use privileged network mode
network_mode: "host" # Can sniff all traffic
```

---

## 🛡️ Application Security

### ✅ Settings Configuration

#### Production Checklist

```python
# settings.py
if not DEBUG:
    # HTTPS/SSL
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Cookies
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # Redirects
    SECURE_REDIRECT_EXEMPT = []

    # Content Security Policy
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
        'script-src': ("'self'", "trusted.com"),
        'style-src': ("'self'", "'unsafe-inline'"),
        'img-src': ("'self'", "data:", "https:"),
    }
```

### ✅ CORS Configuration

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

CORS_ALLOW_CREDENTIALS = True

# NOT this:
CORS_ALLOW_ALL_ORIGINS = True  # ✗ Never!
```

### ✅ Rate Limiting

```python
# settings.py
# Install django-ratelimit: pip install django-ratelimit

# views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/h', method='POST')
def login(request):
    pass

# Nginx (Better for production)
# nginx.conf
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req zone=login burst=10 nodelay;
```

### ✅ Input Validation

```python
# serializers.py
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        extra_kwargs = {
            'name': {'max_length': 255},
            'price': {'min_value': 0}
        }

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        return value
```

### ✅ SQL Injection Prevention

```python
# ✓ Using ORM (Safe)
products = Product.objects.filter(
    name__icontains=user_input
)

# ✓ Using parameterized queries
from django.db import connection
cursor = connection.cursor()
cursor.execute(
    "SELECT * FROM shop_product WHERE name LIKE %s",
    [f"%{user_input}%"]
)

# ✗ String concatenation (Unsafe)
cursor.execute(f"SELECT * FROM shop_product WHERE name LIKE '%{user_input}%'")
```

### ❌ Application Anti-Patterns

```python
# ✗ Hardcoded credentials
API_KEY = "sk-1234567890abcdef"

# ✗ Debug mode in production
DEBUG = True

# ✗ No CSRF protection
@csrf_exempt  # Only when absolutely necessary
def webhook(request):
    pass

# ✗ Weak password policy
AUTH_PASSWORD_VALIDATORS = []

# ✗ Exposed error details
DEBUG = True  # Shows stack traces
```

---

## 🗄️ Database Security

### ✅ PostgreSQL Security

```sql
-- ✓ Strong password policy
ALTER USER ecommerce_user WITH PASSWORD 'strong-password-here';

-- ✓ Limit user permissions
REVOKE ALL PRIVILEGES ON DATABASE ecommerce FROM PUBLIC;
GRANT CONNECT ON DATABASE ecommerce TO ecommerce_user;
GRANT USAGE ON SCHEMA public TO ecommerce_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ecommerce_user;

-- ✓ Audit logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_connections = 'on';

-- ✓ Encryption at rest (if supported by provider)
CREATE ENCRYPTED EXTENSION pgcrypto;
```

### ✅ Connection Pool Security

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',  # Force SSL in production
            'connect_timeout': 10,
        }
    }
}
```

### ✅ Backup Encryption

```bash
# ✓ Encrypt backup
pg_dump -U ecommerce_user ecommerce | \
gpg --symmetric --cipher-algo AES256 \
--output backup.sql.gpg

# ✓ Restore from encrypted backup
gpg --decrypt backup.sql.gpg | \
psql -U ecommerce_user ecommerce
```

### ❌ Database Anti-Patterns

```bash
# ✗ Default credentials
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# ✗ No encryption
sslmode=disable

# ✗ Backup without encryption
pg_dump > backup.sql  # Readable!

# ✗ Database exposed to network
ports:
  - "5432:5432"  # Anyone can access
```

---

## 🔄 CI/CD Security

### ✅ GitHub Actions Security

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
    push:
        branches: [main]

jobs:
    deploy:
        runs-on: ubuntu-latest
        environment: production # Protected environment

        steps:
            - uses: actions/checkout@v4

            # ✓ Use secrets for sensitive data
            - name: Deploy
              env:
                  DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
                  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
              run: |
                  echo "$DEPLOY_KEY" > ~/.ssh/deploy_key
                  chmod 600 ~/.ssh/deploy_key
                  ssh -i ~/.ssh/deploy_key user@server

            # ✓ Scan dependencies
            - name: Security scanning
              run: |
                  pip install safety
                  safety check

            # ✓ Container scanning
            - name: Scan image
              uses: aquasecurity/trivy-action@master
              with:
                  image-ref: "myapp:${{ github.sha }}"
                  exit-code: "1"
                  severity: "CRITICAL"
```

### ✅ Container Registry Security

```bash
# ✓ Use private registry
docker login -u $USERNAME -p $PASSWORD registry.example.com

# ✓ Sign images
docker trust sign registry.example.com/myapp:latest

# ✓ Scan before push
trivy image myapp:latest

# ✓ Rotate tokens regularly
aws ecr get-authorization-token --region us-east-1
```

### ✅ Secret Rotation

```bash
# ✓ Rotate secrets monthly
1. Generate new secret
2. Update in secrets manager
3. Redeploy containers
4. Verify old secret is revoked
5. Archive old secret

# Automated rotation
aws secretsmanager rotate-secret \
  --secret-id django/secret-key \
  --rotation-rules AutomaticallyAfterDays=30
```

### ❌ CI/CD Anti-Patterns

```yaml
# ✗ Secrets in code
env:
  DB_PASSWORD: "password123"

# ✗ No permission restrictions
permissions:
  contents: write

# ✗ Run tests with prod credentials
env:
  DATABASE_URL: ${{ secrets.PROD_DB_URL }}

# ✗ Push to public registry
docker push myapp:latest  # Without auth!
```

---

## 📊 Monitoring & Logging

### ✅ Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### ✅ Audit Logging

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
import json
from datetime import datetime

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    changes = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
```

### ✅ Monitoring & Alerting

```python
# Install: pip install django-health-check prometheus-client

# settings.py
INSTALLED_APPS += ['health_check']

# views.py
from prometheus_client import Counter, Histogram
import time

request_count = Counter(
    'django_requests_total',
    'Total requests',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'django_request_duration_seconds',
    'Request duration'
)

def track_request(get_response):
    def middleware(request):
        start = time.time()
        response = get_response(request)
        duration = time.time() - start

        request_count.labels(
            method=request.method,
            endpoint=request.path
        ).inc()

        request_duration.observe(duration)
        return response

    return middleware
```

### ✅ Alerting Setup

```bash
# docker-compose.yml additions for monitoring
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
```

### ❌ Logging Anti-Patterns

```python
# ✗ Log passwords
logger.info(f"User logged in: password={password}")

# ✗ No log rotation
# Logs fill disk and crash app

# ✗ Excessive logging
logger.debug("Variable x = " + str(x))  # In production

# ✗ No structured logging
logger.info("Something happened")  # Hard to parse

# ✓ Use structured logging
logger.info("user_login", extra={
    "user_id": user.id,
    "ip_address": request.META['REMOTE_ADDR'],
    "timestamp": datetime.now().isoformat()
})
```

---

## 🔐 Security Checklist

### Before Deployment

- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY
- [ ] Review ALLOWED_HOSTS
- [ ] Enable DEBUG=False
- [ ] Setup SSL/TLS certificates
- [ ] Configure CORS properly
- [ ] Review database user permissions
- [ ] Enable rate limiting
- [ ] Setup logging and monitoring
- [ ] Security scan Docker images (trivy)
- [ ] Scan dependencies (safety, pip-audit)
- [ ] Review CSRF and CORS settings
- [ ] Test error handling (no stack traces)
- [ ] Backup database with encryption
- [ ] Setup secrets rotation
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Document security procedures

### Regular Maintenance

- [ ] Weekly: Review access logs
- [ ] Monthly: Rotate secrets
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Security audit
- [ ] Quarterly: Penetration testing
- [ ] Annually: Full security review

---

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-syntax.html)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

---

**Version**: 1.0  
**Last Updated**: 2026-04-22
