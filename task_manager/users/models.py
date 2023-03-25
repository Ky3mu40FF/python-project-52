"""task_manager - users app - models module."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model inherited from AbstractBaseUser to customize."""

    username = models.CharField(
        verbose_name=_('Username'),
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=100,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=100,
        null=False,
        blank=False,
    )
    password = models.CharField(
        verbose_name=_('Password'),
        max_length=100,
        null=False,
        blank=False,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
    )

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.

        Returns:
            (str): first_name plus the last_name, with a space in between.
        """
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        """
        Return string representation of User instance.

        Returns:
            (str): Full name of user (first_name + las_name).
        """
        return self.get_full_name()
