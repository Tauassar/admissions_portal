from django import forms
from django.forms import ModelForm, Form, Select
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import (
    CustomUserModel,
    InterviewEvaluationModel,
    CandidateEvaluationModel,
    CandidateModel,
    AdmissionRoundModel,
    ApplicationEvaluationModel,
    CandidateTestingInformationModel,
    CandidateEducationModel
    )

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


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.pop("autofocus", None)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUserModel
        fields =  '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUserModel
        fields = ('email',)

'''Candidate forms'''
ApplicationFormset = inlineformset_factory(
    CandidateEvaluationModel,
    ApplicationEvaluationModel,
    fields = '__all__',
    can_delete = False)
InterviewFormset = inlineformset_factory(
    CandidateEvaluationModel,
    InterviewEvaluationModel,
    fields = '__all__',
    can_delete = False)


''' 
for creation of a new candidate
'''
class AddCandidateForm(ModelForm):
    class Meta:
        model = CandidateModel
        exclude = [
            'admission_round',
            'gpa',
            'school_rating',
            'research_experience',
            'waiting_list',
            'recomended_for_admission_list',
            'rejected_list',
            'evaluation_finished',
            'candidate_status',
            'total_score']

TestingFormset = inlineformset_factory(
    CandidateModel, 
    CandidateTestingInformationModel,
    fields = '__all__', 
    max_num = 1,
    min_num=1,
    can_delete = False)
EducationFormset = inlineformset_factory(
    CandidateModel,
    CandidateEducationModel,
    extra=1,
    fields = '__all__',
    can_delete = False)


class AdmissionRoundForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['threshold'].required = True
    class Meta:
        model = AdmissionRoundModel
        fields = ['threshold']

'''
Secretary forms
'''
# Set evaluation status to accepted or rejected
class ApprovementForm(Form):
    approved = 'Approved'
    rejected = 'Rejected'
    STATUS_CHOICES = [
    ('', ('-')),
    (approved, ('Approved')),
    (rejected, ('Rejected')),
    ]
    status = forms.ChoiceField(
        choices = STATUS_CHOICES,
        label="Evaluation status: ",
        initial='-',
        widget=Select(),
        required=True)

# Evaluation fields dedicated for secretaries only 
class SecretaryEvaluationForm(ModelForm):
    class Meta:
        model = CandidateModel
        fields = ['gpa','school_rating','research_experience']