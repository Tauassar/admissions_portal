from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

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
# admin.site.register(CandidateEvaluationModel, SimpleHistoryAdmin)
