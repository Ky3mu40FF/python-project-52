"""task_manager - users app - config for admin site."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from task_manager.users.models import User


class CustomUserAdmin(UserAdmin):
    """View for User model in admin site."""

    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'created_at', 'is_staff', 'is_active')
    list_filter = ('username', 'created_at', 'is_staff', 'is_active')
    search_fields = ('username',)

    # Fields sets for Creating user form (CustomUserCreationForm)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
            ),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active'),
        }),
    )

    # Fields sets for Editing user form (CustomUserChangeForm)
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
                'first_name',
                'last_name',
            ),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
