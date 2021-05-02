from django import forms
from django.forms import ModelForm, modelform_factory, SelectDateWidget, modelformset_factory
from candidates_app.models import (CandidateModel,
                                   CandidateTestsModel,
                                   CandidateEducationModel)
from django.forms import inlineformset_factory

from candidates_app.widgets import FileWidget


class AddCandidateForm(ModelForm):
    class Meta:
        model = CandidateModel
        exclude = [
            'created_by',
            'admission_round',
            'gpa',
            'school_rating',
            'research_experience',
            'student_list',
            'evaluation_finished',
            'candidate_status',
            'total_score']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': "first_name",
                'class': "create-cand-item"}),
            'last_name': forms.TextInput(attrs={
                'id': "last_name",
                'class': "create-cand-item"}),
            'applying_degree': forms.Select(attrs={
                'id': "app_degree",
                'class': "create-cand-item"}),
            'diploma': FileWidget(),
            'ielts_certificate': FileWidget(),
            'toefl_certificate': FileWidget(),
            'english_level_certificate': FileWidget(),
            'gmat_or_gre': FileWidget(),
            'statement_of_purpose': FileWidget(),
            'cv': FileWidget(),
            'recomendation_1': FileWidget(),
            'recomendation_2': FileWidget(),
        }


class CandidateTesting(ModelForm):
    class Meta:
        model = CandidateTestsModel
        fields = ['ielts',
                  'toefl',
                  'gre']


EducationFormset = modelformset_factory(
    CandidateEducationModel,
    max_num =2,
    exclude=('candidate',),
    widgets={
        'start_date': forms.DateInput(attrs={
            'type': 'date',
            'id': "start-date",
            'class': "create-cand-item"
        }),
        'end_date': forms.DateInput(attrs={
            'type': 'date',
            'id': "end-date",
            'class': "create-cand-item"}),
        'grad_date': forms.DateInput(attrs={
            'type': 'date',
            'id': "grad-date",
            'class': "create-cand-item"}),
        'degree_type': forms.Select(attrs={
            'id': "com-degree",
            'class': "create-cand-item"}),
        'institution': forms.TextInput(attrs={
            'id': "institution",
            'class': "create-cand-item"})
        # study_field
        # gpa
    }
)

EducationFormset_old = inlineformset_factory(
    CandidateModel,
    CandidateEducationModel,
    extra=1,
    fields='__all__',
    can_delete=False)
