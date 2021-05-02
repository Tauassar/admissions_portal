from django import forms
from django.forms import inlineformset_factory

from evaluations_app.models import (CandidateEvaluationModel,
                                    ApplicationEvaluationModel,
                                    InterviewEvaluationModel)

ApplicationFormset = inlineformset_factory(
    CandidateEvaluationModel,
    ApplicationEvaluationModel,
    fields='__all__',
    can_delete=False)
InterviewFormset = inlineformset_factory(
    CandidateEvaluationModel,
    InterviewEvaluationModel,
    fields='__all__',
    can_delete=False)


class InterviewForm(forms.ModelForm):

    class Meta:
        model = InterviewEvaluationModel
        exclude = ['evaluation', ]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = ApplicationEvaluationModel
        exclude = ['evaluation', ]
