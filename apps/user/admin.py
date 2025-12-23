from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.forms import UserCreationForm, UserChangeForm
from apps.user.models import User

# Register your models here.

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('username', 'is_active', 'is_staff', 'is_superuser', 'role', 'profile_picture')
    list_filter = ('username', 'is_staff', 'is_active', 'role')

    fieldsets = (
        (None,
         {'fields': ('username', 'password', 'role', 'profile_picture')}),
        ('Permissions',
         {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'role', 'profile_picture')}
         ),
    )

    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, UserAdmin)
