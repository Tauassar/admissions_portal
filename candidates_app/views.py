from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from admission_periods_app.models import AdmissionYearModel
from auth_app.decorators import check_permissions
from auth_app.models import CustomUserModel
from candidates_app.forms import (TestingFormset,
                                  EducationFormset,
                                  AddCandidateForm)
from candidates_app.models import CandidateModel


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.ADMISSION_DEPARTMENT])
def createCandidateView(request, candidate_id=None):
    if candidate_id is not None:
        candidate = get_object_or_404(
            CandidateModel, candidate_id=candidate_id)
        form = AddCandidateForm(instance=candidate)
        testing_formset = TestingFormset(instance=candidate)
        education_formset = EducationFormset(instance=candidate)
    else:
        form = AddCandidateForm()
        testing_formset = TestingFormset()
        education_formset = EducationFormset()
    if request.method == "POST":
        form = AddCandidateForm(request.POST, request.FILES)
        testing_formset = TestingFormset(request.POST, instance=candidate)
        education_formset = EducationFormset(request.POST, instance=candidate)
        if form.is_valid() and testing_formset.is_valid() and \
                education_formset.is_valid():
            admission_year = get_object_or_404(AdmissionYearModel, active=True)
            form.save()
            testing_formset.save()
            education_formset.save()
            candidate.student_list = admission_year.current_candidates
            return redirect('dashboard')
    context = {
        'form': form,
        'testing_formset': testing_formset,
        'education_formset': education_formset}
    return render(request, 'candidates_app/create_candidate.html', context)
