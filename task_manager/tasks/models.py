"""task_manager - tasks app - models module."""
from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import User

class Task(models.Model):
    """Task model."""

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        null=False,
        blank=False,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executing_tasks',
        null=True,
        blank=True,
    )
    # tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
