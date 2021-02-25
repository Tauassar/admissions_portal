from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class InterviewEvaluationInline(ModelForm):
    class Meta:
        model = InterviewEvaluationModel
        fields = '__all__'


class CandidateEvaluateForm(ModelForm):
    class Meta:
        model = CandidateEvaluationModel
        exclude = ['evaluator']
        inlines = [InterviewEvaluationInline]


class AddCandidateForm(ModelForm):
    class Meta:
        model = CandidateModel
        exclude = ['admission_round','gpa','school_rating','research_experience']


class AdmissionRoundForm(ModelForm):
    class Meta:
        model = AdmissionRoundModel
        fields = ['threshold']


class ApprovementForm(ModelForm):
    class Meta:
        model = CandidateEvaluationModel
        fields = ['approved_by_secretary', 'status']