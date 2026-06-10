from django.db import models


class Status(models.TextChoices):
    TO_DO = 'To Do', 'to do'
    IN_PROGRESS = 'In Progress', 'in progress'
    TEST = 'Test', 'test'
    REJECTED = 'Rejected', 'rejected'
    DONE = 'Done', 'done'
    BACKLOG = 'Backlog', 'backlog'


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'project'


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.TO_DO, max_length=50)
    to_user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('Project', on_delete=models.PROTECT)

    class Meta:
        db_table = 'task'
