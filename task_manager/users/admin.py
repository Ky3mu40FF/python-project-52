from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'created_at', 'is_staff', 'is_active',)
    list_filter = ('username', 'created_at', 'is_staff', 'is_active',)
    search_fields = ('username',)
    
    # Fields sets for Creating user form (CustomUserCreationForm)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2',)}
        ),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active',),
        }),
    )
    
    # Fields sets for Editing user form (CustomUserChangeForm)
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'first_name', 'last_name',),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active',),
        }),
    )

admin.site.register(User, CustomUserAdmin)
