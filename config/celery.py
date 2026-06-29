import os
from celery import Celery

# Django settings modulini ko'rsatamiz
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings'
)

# Celery instansiyasi yaratamiz
app = Celery('config')

# Settings dan CELERY_ boshlanadigan o'zgaruvchilarni o'qiymiz
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha app lardagi tasks.py fayllarni avtomatik topadi
app.autodiscover_tasks()