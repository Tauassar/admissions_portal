from django.contrib import admin
from admission_periods_app import models


class StaffListAdmin(admin.TabularInline):
    model = models.StaffListModel


class AdmissionRoundAdmin(admin.TabularInline):
    model = models.AdmissionRoundModel
    max_num = 3
    extra = 1


class AdmissionYearAdmin(admin.ModelAdmin):
    model = models.AdmissionYearModel
    inlines = [StaffListAdmin, AdmissionRoundAdmin, ]


admin.site.register(models.AdmissionYearModel, AdmissionYearAdmin)
admin.site.register(models.StudentList)
