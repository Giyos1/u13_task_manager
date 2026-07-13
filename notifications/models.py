from django.db import models


class Notifications(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    to_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        ordering = ('-created_at',)
