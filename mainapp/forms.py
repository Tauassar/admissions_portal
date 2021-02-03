from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class CandidateEvaluateForm(ModelForm):
    class Meta:
        model = EvaluationModel
        fields = [
            'gpa','recommendations','educational_backgorund',
            'understanding_of_major','research_interest_and_motivation', 'experience_and_goals',
            'english_level',
        ]


class AddCandidateForm(ModelForm):
    class Meta:
        model = CandidateModel
        fields = '__all__'


class ApprovementForm(ModelForm):
    class Meta:
        model = EvaluationModel
        fields = ['approved_by_secretary', 'status']