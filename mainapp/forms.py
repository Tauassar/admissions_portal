from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import CustomUserModel, InterviewEvaluationModel, CandidateEvaluationModel, CandidateModel, AdmissionRoundModel

'''User forms'''
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUserModel
        fields =  '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUserModel
        fields = ('email',)

'''Candidate forms'''
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