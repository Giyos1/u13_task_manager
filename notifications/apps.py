from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        # Signal larni ro'yxatdan o'tkazamiz
        import notifications.signals  # noqa
