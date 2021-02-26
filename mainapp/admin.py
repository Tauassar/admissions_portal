from django.contrib import admin
from . import models
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.CustomUserModel
    list_display = [field.name for field in models.CustomUserModel._meta.fields if field.name not in ('id', 'password')]
    list_display.insert(0, '__str__')
    list_filter = [field.name for field in models.CustomUserModel._meta.fields if field.name not in ('id', 'password')]
    fieldsets = (
        ('Info', {'fields': (
            'email', 'profile_pic', 'first_name', 'last_name', 'school', 'department',
            'phone_number', 'password','position')}),
        ('Permissions', {'fields': ('is_staff','is_active','groups','user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.CustomUserModel, CustomUserAdmin)
admin.site.register(models.CandidateModel)
admin.site.register(models.CandidateEvaluationModel)
admin.site.register(models.InformationModel)
admin.site.register(models.CandidateTestingInformationModel)
admin.site.register(models.CandidateEducationModel)
admin.site.register(models.StaffListModel)
admin.site.register(models.AdmissionRoundModel)
admin.site.register(models.AdmissionYearModel)