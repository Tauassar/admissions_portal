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
        ('Permissions', {'fields': ('is_staff','is_active',)}),
        # ('Permissions', {'fields': ('is_staff','is_active','groups','user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

'''
    Candidate evaluation registration to admin site
'''
class ApplicationEvaluationAdmin(admin.TabularInline):
    model=models.ApplicationEvaluationModel


class InterviewEvaluationAdmin(admin.TabularInline):
    model=models.InterviewEvaluationModel


class CandidateEvaluationAdmin(admin.ModelAdmin):
    model=models.CandidateEvaluationModel
    inlines = [ApplicationEvaluationAdmin, InterviewEvaluationAdmin,]
'''
    AdmissionYear registration to admin site
'''
class StaffListAdmin(admin.TabularInline):
    model=models.StaffListModel


class AdmissionRoundAdmin(admin.TabularInline):
    model=models.AdmissionRoundModel
    max_num=3
    extra=1


class AdmissionYearAdmin(admin.ModelAdmin):
    model=models.AdmissionYearModel
    inlines = [StaffListAdmin, AdmissionRoundAdmin,]

'''
    CandidateModel registration to admin site
'''
class CandidateTestingInformationAdmin(admin.TabularInline):
    model=models.CandidateTestingInformationModel

class CandidateEducationAdmin(admin.TabularInline):
    model=models.CandidateEducationModel
    max_num=3
    extra=1

class CandidateAdmin(admin.ModelAdmin):
    model=models.CandidateModel
    inlines = [CandidateEducationAdmin, CandidateTestingInformationAdmin,]

admin.site.register(models.CustomUserModel, CustomUserAdmin)
admin.site.register(models.CandidateEvaluationModel,CandidateEvaluationAdmin)
admin.site.register(models.CandidateModel, CandidateAdmin)
admin.site.register(models.AdmissionYearModel, AdmissionYearAdmin)
admin.site.register(models.InformationModel)
admin.site.register(models.StudentList)
