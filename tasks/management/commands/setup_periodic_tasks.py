from django.core.management.base import BaseCommand
from django_celery_beat.models import (
    PeriodicTask, IntervalSchedule, CrontabSchedule
)

class Command(BaseCommand):
    help = 'Celery Beat periodic tasklarni DB ga yozadi'

    def handle(self, *args, **kwargs):

        # 1. Har 10 soniyada
        interval, _ = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS
        )
        PeriodicTask.objects.update_or_create(
            name='Har 10 soniyada status tekshirish',
            defaults={
                'interval': interval,
                'task': 'tasks.tasks.send_report',
                'enabled': True,
            }
        )

        # 2. Har kuni soat 09:00 da
        crontab, _ = CrontabSchedule.objects.get_or_create(
            minute='0', hour='9',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
        PeriodicTask.objects.update_or_create(
            name='Kunlik hisobot yuborish',
            defaults={
                'crontab': crontab,
                'task': 'tasks.tasks.send_report',
                'enabled': True,
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                '✅ Periodic tasklar muvaffaqiyatli yaratildi!'
            )
        )