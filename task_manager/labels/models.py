"""task_model - labels - models module."""
from django.db import models


class Label(models.Model):
    """Label for task model."""

    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return string representation of Label instance.

        Returns:
            (str): Label's name
        """
        return self.name
