from django.forms import ModelForm
from candidates_app.models import (CandidateModel,
                                   CandidateTestsModel,
                                   CandidateEducationModel)
from django.forms import inlineformset_factory


class AddCandidateForm(ModelForm):
    class Meta:
        model = CandidateModel
        exclude = [
            'admission_round',
            'gpa',
            'school_rating',
            'research_experience',
            'student_list',
            'evaluation_finished',
            'candidate_status',
            'total_score']


TestingFormset = inlineformset_factory(
    CandidateModel,
    CandidateTestsModel,
    fields='__all__',
    max_num=1,
    min_num=1,
    can_delete=False)


EducationFormset = inlineformset_factory(
    CandidateModel,
    CandidateEducationModel,
    extra=1,
    fields='__all__',
    can_delete=False)
