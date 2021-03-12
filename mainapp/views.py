from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from admission_periods_app.forms import AdmissionRoundForm
from admission_periods_app.utils import get_current_year_and_round
from auth_app.decorators import check_permissions
from auth_app.models import CustomUserModel
from mainapp.utils import compose_lists

"""
    TODO: 
        add committee report error button
        secretary comments
        forgot pass
        mail send
        different dashboards for different users
        recent actions
        change image profile
"""


@login_required(login_url='login')
def dashboardView(request):
    admission_year, admission_round = get_current_year_and_round()
    try:
        candidates = admission_round.candidatemodel_set.all()
        if request.user.position not in [1, 2]:
            evaluations = admission_round.candidateevaluationmodel_set.all()
        else:
            evaluations = admission_round.candidateevaluationmodel_set.filter(
                evaluator=request.user)
    except (ObjectDoesNotExist, AttributeError):
        return render(request, 'mainapp/main_dashboard.html')
    context = {
        'candidates': candidates,
        'evaluations': evaluations,
        'admission_round': admission_round.round_number
    }
    return render(request, 'mainapp/main_dashboard.html', context)


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.COMMITTEE_CHAIR])
def ChairView(request):
    admission_year, admission_round = get_current_year_and_round()
    try:
        candidates_waiting_list = admission_year.current_candidates. \
            candidatemodel_set.all()
        candidates_accepted = admission_round. \
            accepted_candidates_list.candidatemodel_set.all()
        candidates = candidates_waiting_list | candidates_accepted
        evaluated_candidates_count = len(
            candidates.filter(evaluation_finished=True))
        non_evaluated_candidates_count = len(
            candidates.exclude(evaluation_finished=True))
    except (ObjectDoesNotExist, AttributeError):
        return redirect('dashboard')
    form = AdmissionRoundForm(instance=admission_round)
    context = {
        'form': form,
        'candidates': candidates.order_by("-total_score"),
        'total_candidates': len(candidates),
        'evaluated_candidates_count': evaluated_candidates_count,
        'non_evaluated_candidates_count': non_evaluated_candidates_count
    }
    if request.method == "POST":
        form = AdmissionRoundForm(request.POST, instance=admission_round)
        if non_evaluated_candidates_count:
            messages.error(
                request, 'Evaluation of candidates is not finished yet')
            return render(request, 'mainapp/chair_template.html', context)
        if form.is_valid():
            form.save()
            all_candidates = admission_year. \
                current_candidates.candidatemodel_set.all()
            threshold = form.cleaned_data["threshold"]
            compose_lists(
                threshold, all_candidates, admission_year, admission_round)
            return redirect('dashboard')
    return render(request, 'mainapp/chair_template.html', context)


@login_required(login_url='login')
@check_permissions(allowed_pos=[CustomUserModel.COMMITTEE_CHAIR])
def SecretaryView(request):
    admission_year, admission_round = get_current_year_and_round()
    try:
        waiting_list_candidates = admission_year. \
            current_candidates.candidatemodel_set.all()
        recommended_list = \
            admission_round.accepted_candidates_list.candidatemodel_set.all()
        rejected_list_candidates = admission_round. \
            rejected_candidates_list.candidatemodel_set.all()
        context = {
            'recommended_list_candidates': recommended_list,
            'waiting_list_candidates': waiting_list_candidates,
            'rejected_list_candidates': rejected_list_candidates,
        }
        return render(request, 'mainapp/secretary_template.html', context)
    except Exception as e:
        print(e)
        return render(request, 'mainapp/secretary_template.html')
