from django.contrib import admin
from candidates_app.models import (
    CandidateTestsModel,
    CandidateEducationModel,
    CandidateModel
)


class CandidateTestingInformationAdmin(admin.TabularInline):
    model = CandidateTestsModel


class CandidateEducationAdmin(admin.TabularInline):
    model = CandidateEducationModel
    max_num = 3
    extra = 1


class CandidateAdmin(admin.ModelAdmin):
    model = CandidateModel
    inlines = [CandidateEducationAdmin, CandidateTestingInformationAdmin, ]


admin.site.register(CandidateModel, CandidateAdmin)
