"""task_manager - statuses app - models module."""
from django.db import models

class Status(models.Model):
    """Status of task model."""

    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
