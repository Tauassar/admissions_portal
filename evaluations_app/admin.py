from django.contrib import admin

from evaluations_app.models import (CandidateEvaluationModel,
                                    InterviewEvaluationModel,
                                    ApplicationEvaluationModel)


class ApplicationEvaluationAdmin(admin.TabularInline):
    model = ApplicationEvaluationModel


class InterviewEvaluationAdmin(admin.TabularInline):
    model = InterviewEvaluationModel


class CandidateEvaluationAdmin(admin.ModelAdmin):
    model = CandidateEvaluationModel
    inlines = [ApplicationEvaluationAdmin, InterviewEvaluationAdmin, ]


admin.site.register(CandidateEvaluationModel, CandidateEvaluationAdmin)
