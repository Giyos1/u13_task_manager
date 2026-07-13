from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notifications


@receiver(post_save, sender=Notifications)
def send_notification_on_create(sender, instance, created, **kwargs):
    # Faqat yangi notification yaratilganda ishlaydi
    if not created:
        return

    channel_layer = get_channel_layer()
    group_name = f'notifications_{instance.to_user_id}'

    # Consumer dagi send_notification (type) funksiyasiga yuboramiz
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'message': {
                'id': instance.id,
                'title': instance.title,
                'description': instance.description,
                'is_read': instance.is_read,
                'created_at': instance.created_at.isoformat(),
            },
        }
    )