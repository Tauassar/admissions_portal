from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from admission_periods_app.forms import AdmissionRoundForm
from admission_periods_app.utils import (get_current_year_and_round,
                                         get_candidates)
from auth_app.models import CustomUserModel
from mainapp.mixins import PositionMixin
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
        write permissions mixin
"""


@login_required(login_url='login')
def dashboardView(request):
    admission_year, admission_round = get_current_year_and_round()
    try:
        candidates = admission_round.candidates.all()
        if request.user.position not in [CustomUserModel.COMMITTEE_CHAIR,
                                         CustomUserModel.COMMITTEE_MEMBER]:
            evaluations = admission_round.evaluations.all()
        else:
            evaluations = admission_round.evaluations.filter(
                evaluator=request.user)
    except (ObjectDoesNotExist, AttributeError):
        print("ERROR")
        return render(request, 'mainapp/main_dashboard.html')
    context = {
        'candidates': candidates,
        'evaluations': evaluations,
        'admission_round': admission_round.round_number
    }
    return render(request, 'mainapp/main_dashboard.html', context)


class ChairView(LoginRequiredMixin, PositionMixin, UpdateView):
    permission_groups = [CustomUserModel.COMMITTEE_CHAIR]
    form_class = AdmissionRoundForm
    template_name = 'mainapp/chair_template.html'
    context_object_name = 'candidates'
    success_url = reverse_lazy('chair')
    non_evaluated_count = None
    admission_year = None
    admission_round = None

    def form_valid(self, form):
        if self.non_evaluated_count:
            messages.error(
                self.request, 'Evaluation of candidates is not finished yet')
            return self.form_invalid(form)
        else:
            threshold = form.cleaned_data["threshold"]
            compose_lists(
                threshold,
                self.admission_year,
                self.admission_round)
            return super(ChairView, self).form_valid(form)

    def get_object(self, queryset=None):
        self.admission_year, self.admission_round =\
            get_current_year_and_round()
        return self.admission_round

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidates, evaluated_count, non_evaluated_count = \
            get_candidates(self.admission_year, self.admission_round)
        self.non_evaluated_count = non_evaluated_count
        context['candidates'] = candidates
        context['total'] = candidates.count()
        context['evaluated_count'] = evaluated_count
        context['non_evaluated_count'] = non_evaluated_count
        return context


class SecretaryView(LoginRequiredMixin, PositionMixin, ListView):
    template_name = 'mainapp/secretary_template.html'
    context_object_name = 'candidates'
    permission_groups = [CustomUserModel.SECRETARY]

    def get_queryset(self):
        admission_year, admission_round = get_current_year_and_round()
        try:
            waiting_list_candidates = admission_year. \
                current_candidates.candidates.all()
            recommended_list = \
                admission_round.accepted_candidates_list.candidates.all()
            rejected_list_candidates = admission_round. \
                rejected_candidates_list.candidates.all()
            return {
                'recommended_list': recommended_list,
                'waiting_list': waiting_list_candidates,
                'rejected_list': rejected_list_candidates,
            }
        except Exception as e:
            print(e)
            return None
