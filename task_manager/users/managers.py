"""task_manager - users app - manager module for custom user model."""
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager for custom user (inherited from AbstractBaseUser)."""

    def create_user(
        self,
        username: str,
        password: str,
        **extra_fields,
    ):
        """Create and save User with given username and password.

        Args:
            username (str): Users username.
            password (str): Users password.
            **extra_fields: Users model extra fields.

        Returns:
            (User): New User instance.

        Raises:
            ValueError: If username is empty.
        """
        if not username:
            raise ValueError()
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        username: str,
        password: str,
        **extra_fields,
    ):
        """Create and save SuperUser with given username and password.

        Args:
            username (str): Users username.
            password (str): Users password.
            **extra_fields: Users model extra fields.

        Returns:
            (User): New User instance with superuser role.

        Raises:
            ValueError: If is_staff and is_superuser not True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)
