from django.contrib import admin
from auth_app import models
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

from .models import AuditEntry


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.CustomUserModel
    list_display = [field.name for field in
                    models.CustomUserModel._meta.fields
                    if field.name not in ('id', 'password')]
    list_display.insert(0, '__str__')
    list_filter = [field.name for field
                   in models.CustomUserModel._meta.fields
                   if field.name not in ('id', 'password')]
    fieldsets = (
        ('Info', {'fields': (
            'email',
            'profile_pic',
            'first_name',
            'last_name',
            'school',
            'department',
            'phone_number',
            'password',
            'position')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'is_staff',
                       'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip']
    list_filter = ['action']


admin.site.register(models.CustomUserModel, CustomUserAdmin)
