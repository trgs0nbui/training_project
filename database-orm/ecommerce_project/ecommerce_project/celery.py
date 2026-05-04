import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

app = Celery('ecommerce_project')

# Đọc config từ Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động tìm tasks trong apps
app.autodiscover_tasks()