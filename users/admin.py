from django.contrib import admin
from .models import *
# from django.utils import timezone
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdminConfig(UserAdmin):
    ordering = ('email','first_name','last_name',)
    list_display = ('email','first_name','last_name','is_active','is_staff','is_superuser',)
    fieldsets = (
        (
            'Fields',
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'mobile',
                    'country',
                    'profile_photo',
                    'bio',
                    'company',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'password',
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','mobile', 'password1','password2',),
            #              🖞 without username
        }),
    )

admin.site.register(User, UserAdminConfig)