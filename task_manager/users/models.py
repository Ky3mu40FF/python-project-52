"""task_manager - users app - models module."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from task_manager.users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model inherited from AbstractBaseUser to customize."""

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    @property
    def full_name(self) -> str:
        """Return full name (joined first name and last name).

        Returns:
            (str): User's full name (joined first name and last name).
        """
        return ' '.join((self.first_name, self.last_name))
