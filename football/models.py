from django.db import models


class Status(models.TextChoices):
    ACTIVE = 'active', "Active"
    PASSIVE = 'passive', "Passive"


class BronStatus(models.TextChoices):
    FREE = 'free', "Free"
    BLOCKED = 'blocked', "Blocked"


class Stadium(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    lat = models.DecimalField()
    long = models.DecimalField()
    price = models.IntegerField()
    status = models.CharField(choices=Status.choices, default=Status.ACTIVE)
    owner = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)


class Bron(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(choices=BronStatus.choices, default=BronStatus.FREE)
    assign_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, default=None, blank=True)

    class Meta:
        unique_together = ('stadium', 'date', 'start_time')
