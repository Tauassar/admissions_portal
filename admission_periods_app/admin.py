from django.contrib import admin

from admission_periods_app import models
from candidates_app.models import CandidateModel


class StaffListAdmin(admin.TabularInline):
    model = models.StaffListModel


class AdmissionRoundAdmin(admin.TabularInline):
    model = models.AdmissionRoundModel
    max_num = 3
    extra = 1


class AdmissionYearAdmin(admin.ModelAdmin):
    model = models.AdmissionYearModel
    inlines = [StaffListAdmin, AdmissionRoundAdmin, ]


class CandidateAdmin(admin.TabularInline):
    model = CandidateModel


class StudentList(admin.ModelAdmin):
    model = models.StudentList
    inlines = [CandidateAdmin, ]


admin.site.register(models.AdmissionYearModel, AdmissionYearAdmin)
admin.site.register(models.StudentList, StudentList)
