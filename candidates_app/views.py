import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from auth_app.decorators import check_permissions
from auth_app.models import CustomUserModel
from candidates_app.forms import (CandidateTesting,
                                  EducationFormset,
                                  AddCandidateForm)
from candidates_app.models import CandidateModel, CandidateEducationModel

logger = logging.getLogger(__name__)


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.ADMISSION_DEPARTMENT])
def createCandidateView(request, candidate_id=None):
    return render(request, 'candidates_app/create_candidate.html')


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.ADMISSION_DEPARTMENT])
def observeCandidateView(request, candidate_id=None):
    if candidate_id is not None:
        candidate = get_object_or_404(
            CandidateModel, candidate_id=candidate_id)
        form = AddCandidateForm(instance=candidate)
        testing_form = CandidateTesting(
            instance=candidate.testing_info)
        education_formset = EducationFormset(
            queryset=CandidateEducationModel.objects.filter(candidate=candidate))
    else:
        form = AddCandidateForm()
        testing_form = CandidateTesting()
        education_formset = EducationFormset()
    if request.method == "POST":
        form = AddCandidateForm(request.POST, request.FILES, instance=candidate)
        testing_form = CandidateTesting(
            request.POST, instance=candidate.testing_info)
        education_formset = EducationFormset(
            request.POST,
            CandidateEducationModel.objects.filter(candidate=candidate),
            initial=[
                {'candidate': candidate},
                {'candidate': candidate}
            ])

        if form.is_valid() and testing_form.is_valid() and \
                education_formset.is_valid():
            form.save()
            testing_form.save()
            for edu_formset in education_formset:
                edu = edu_formset.save(commit=False)
                edu.candidate = candidate
                edu.save()
            logger.info(str(candidate) + ' updated by ' + str(request.user))
            return redirect('dashboard')
    context = {
        'candidate': candidate,
        'form': form,
        'testing_form': testing_form,
        'education_formset': education_formset}
    return render(request, 'candidates_app/observe_candidate.html', context)
