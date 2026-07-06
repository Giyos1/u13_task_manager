import time

from celery import shared_task
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filemode='a',
    filename='log.log'
)

logger = logging.getLogger(__name__)


# Oddiy task
@shared_task
def add(x, y):
    time.sleep(60)
    return x + y


@shared_task
def send_email_task(email, subject):
    time.sleep(5)  # email yuborish vaqti
    return f"✅ Email {email} ga yuborildi: {subject}"


@shared_task
def send_report():
    # tasklarni tabledan olib bitta html qilib emailga jonatila ozlarizni emailarga
    logger.info('📊 Hisobot yuborilmoqda...')
    logger.info('📊 Hisobot yaratildi...')
