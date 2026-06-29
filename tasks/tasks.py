import time

from celery import shared_task


# Oddiy task
@shared_task
def add(x, y):
    time.sleep(60)
    return x + y

@shared_task
def send_email_task(email, subject):
    time.sleep(5)   # email yuborish vaqti
    return f"✅ Email {email} ga yuborildi: {subject}"