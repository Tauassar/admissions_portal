from django import forms
from django.forms import ModelForm, Form, Select
from candidates_app.models import CandidateModel, DEGREE
from evaluations_app.models import CandidateEvaluationModel


class DashboardFilterForms(Form):
    name = forms.CharField(required=False, max_length=10)
    surname = forms.CharField(required=False, max_length=10)
    major = forms.ChoiceField(choices=DEGREE)
    status = forms.ChoiceField(choices=CandidateEvaluationModel.STATUS)


# Secretary forms
class ApprovementForm(Form):
    # Set evaluation status to accepted or rejected
    approved = 'Approved'
    rejected = 'Rejected'
    STATUS_CHOICES = [
        ('', '-'),
        (approved, 'Approved'),
        (rejected, 'Rejected'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="Evaluation status: ",
        initial='-',
        widget=Select(),
        required=True)


class SecretaryEvaluationForm(ModelForm):
    # Evaluation fields dedicated for secretaries only
    class Meta:
        model = CandidateModel
        fields = ['gpa', 'school_rating', 'research_experience']
