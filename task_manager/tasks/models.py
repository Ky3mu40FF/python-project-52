"""task_manager - tasks app - models module."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.users.models import User

class Task(models.Model):
    """Task model."""

    name = models.CharField(
        max_length=100,
        verbose_name=_('Password'),
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description'),
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name=_('Author'),
        null=False,
        blank=True,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executing_tasks',
        verbose_name=_('Executor'),
        null=True,
        blank=True,
    )
    # tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'),)

    def __str__(self):
        return self.name
