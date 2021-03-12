from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from auth_app.decorators import check_permissions
from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from evaluations_app.forms import InterviewFormset, ApplicationFormset
from evaluations_app.models import (CandidateEvaluationModel,
                                    ApplicationEvaluationModel,
                                    InterviewEvaluationModel)
from evaluations_app.utils import queryset_to_dict
from mainapp.forms import SecretaryEvaluationForm, ApprovementForm


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.COMMITTEE_MEMBER,
                                CustomUserModel.COMMITTEE_CHAIR])
def candidateEvaluateView(request, uuid):
    evaluator = request.user
    candidate = get_object_or_404(CandidateModel, candidate_id=uuid)
    evaluation = get_object_or_404(
        CandidateEvaluationModel,
        evaluator=evaluator,
        candidate=candidate)
    application_formset = ApplicationFormset(instance=evaluation)
    interview_formset = InterviewFormset(instance=evaluation)
    if request.method == "POST":
        application_formset = ApplicationFormset(
            request.POST, instance=evaluation)
        interview_formset = InterviewFormset(
            request.POST, instance=evaluation)
        if application_formset.is_valid() and interview_formset.is_valid():
            evaluation.evaluation_status = CandidateEvaluationModel.in_progress
            application_formset.save()
            interview_formset.save()
            evaluation.save()
            return redirect('dashboard')
    context = {
        'application_formset': application_formset,
        'interview_formset': interview_formset,
        'candidate': candidate}
    return render(request, 'evaluations_app/evaluate_candidate.html', context)


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.SECRETARY])
def approveEvalView(request, uuid):
    evaluation = get_object_or_404(
        CandidateEvaluationModel, evaluation_id=uuid)
    application_evaluation = get_object_or_404(
        ApplicationEvaluationModel, evaluation=evaluation)
    interview_evaluation = get_object_or_404(
        InterviewEvaluationModel, evaluation=evaluation)
    application_evaluation_dict = queryset_to_dict(
        application_evaluation,
        exclude=['evaluation', 'id'])
    if not interview_evaluation.skip_evaluation:
        interview_evaluation_dict = queryset_to_dict(
            interview_evaluation,
            exclude=['evaluation', 'id'])
    else:
        interview_evaluation_dict = None
    approve_form = ApprovementForm()
    evaluate_form = SecretaryEvaluationForm(instance=evaluation.candidate)
    if request.method == "POST":
        approve_form = ApprovementForm(request.POST)
        evaluate_form = SecretaryEvaluationForm(
            request.POST, instance=evaluation.candidate)
        if approve_form.is_valid() and evaluate_form.is_valid():
            evaluation.evaluation_status = approve_form.cleaned_data['status']
            evaluate_form.save()
            evaluation.save()
            return redirect('dashboard')

    context = {
        'evaluate_form': evaluate_form,
        'approve_form': approve_form,
        'application_evaluation_dict': application_evaluation_dict,
        'interview_evaluation_dict': interview_evaluation_dict,
        'evaluation': evaluation}

    return render(request, 'evaluations_app/approve_evaluation.html', context)
