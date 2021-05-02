import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework.reverse import reverse_lazy

from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from candidates_app.utils import candidate_unfinish
from evaluations_app.forms import ApplicationForm, InterviewForm
from evaluations_app.models import (CandidateEvaluationModel,
                                    ApplicationEvaluationModel,
                                    InterviewEvaluationModel)
from evaluations_app.utils import queryset_to_dict
from mainapp.forms import SecretaryEvaluationForm, ApprovementForm
from mainapp.mixins import PositionMixin


logger = logging.getLogger(__name__)


class CandidateEvaluateView(LoginRequiredMixin,
                            PositionMixin,
                            TemplateView):
    permission_groups = [CustomUserModel.COMMITTEE_CHAIR,
                         CustomUserModel.COMMITTEE_MEMBER]
    template_name = 'evaluations_app/evaluate_candidate.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'candidate_id'
    context_object_name = 'candidate'

    def get(self, request, *args, **kwargs):
        candidate = get_object_or_404(
            CandidateModel,
            candidate_id=self.kwargs['uuid'])
        evaluation = get_object_or_404(
            CandidateEvaluationModel,
            evaluator=self.request.user,
            candidate=candidate)
        # application_formset = ApplicationFormset(instance=evaluation)
        application_form = ApplicationForm(
            instance=evaluation.application_evaluation)
        interview_form = InterviewForm(
            instance=evaluation.interview_evaluation)
        context = super(CandidateEvaluateView, self).get_context_data(**kwargs)
        education = candidate.education_info.all()
        context['application_form'] = application_form
        context['educations'] = education
        context['interview_form'] = interview_form
        context['candidate'] = candidate
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        candidate = get_object_or_404(
            CandidateModel,
            candidate_id=self.kwargs['uuid'])
        evaluation = get_object_or_404(
            CandidateEvaluationModel,
            evaluator=self.request.user,
            candidate=candidate)
        logger.debug(request.POST)
        if 'relevancy' in request.POST:
            application_form = ApplicationForm(
                request.POST, instance=evaluation.application_evaluation)
            if application_form.is_valid():
                evaluation.evaluation_status = \
                    CandidateEvaluationModel.in_progress
                application_form.save()
                evaluation.save()
                candidate_unfinish(candidate)
            if 'redirect' in request.POST:
                return redirect(reverse_lazy('dashboard'))
        if 'work_experience_goals' in request.POST:
            interview_form = InterviewForm(
                request.POST, instance=evaluation.interview_evaluation)
            if interview_form.is_valid():
                evaluation.evaluation_status = \
                    CandidateEvaluationModel.in_progress
                interview_form.save()
                evaluation.save()
                candidate_unfinish(candidate)
            if 'redirect' in request.POST:
                return redirect(reverse_lazy('dashboard'))
        education = candidate.education_info.all()
        application_form = ApplicationForm(
            instance=evaluation.application_evaluation)
        interview_form = InterviewForm(
            instance=evaluation.interview_evaluation)
        return render(request, self.template_name, {
            "application_form": application_form,
            "interview_form": interview_form,
            "educations": education,
            "candidate": candidate
        })


class ApproveEvaluationView(LoginRequiredMixin,
                            PositionMixin,
                            TemplateView):
    permission_groups = [CustomUserModel.SECRETARY]
    template_name = 'evaluations_app/approve_evaluation.html'

    def get_objects(self):
        evaluation = get_object_or_404(
            CandidateEvaluationModel,
            evaluation_id=self.kwargs['uuid'])
        try:
            application_evaluation = ApplicationEvaluationModel.objects.get(
                evaluation=evaluation)
        except ObjectDoesNotExist:
            application_evaluation = None
        try:
            interview_evaluation = InterviewEvaluationModel.objects.get(
                evaluation=evaluation)
        except ObjectDoesNotExist:
            interview_evaluation = None
        return evaluation, application_evaluation, interview_evaluation

    def get(self, request, *args, **kwargs):
        context = super(ApproveEvaluationView, self).get_context_data(**kwargs)
        evaluation, application_evaluation, interview_evaluation = \
            self.get_objects()
        if application_evaluation:
            application_evaluation_dict = queryset_to_dict(
                application_evaluation,
                exclude=['evaluation', 'id', 'created_at', 'updated_at'])
            context['application_evaluation_dict'] =\
                application_evaluation_dict
        if interview_evaluation:
            if not interview_evaluation.skip_evaluation:
                interview_evaluation_dict = queryset_to_dict(
                    interview_evaluation,
                    exclude=['evaluation',
                             'id',
                             'created_at',
                             'updated_at',
                             'skip_evaluation'])
            else:
                interview_evaluation_dict = None
            context['interview_evaluation_dict'] = interview_evaluation_dict
        approve_form = ApprovementForm()
        evaluate_form = SecretaryEvaluationForm(instance=evaluation.candidate)

        education = evaluation.candidate.education_info.all()
        context['educations'] = education
        context['evaluate_form'] = evaluate_form
        context['approve_form'] = approve_form
        context['evaluation'] = evaluation
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        evaluation, application_evaluation, interview_evaluation = \
            self.get_objects()
        approve_form = ApprovementForm(self.request.POST)
        evaluate_form = SecretaryEvaluationForm(
            request.POST, instance=evaluation.candidate)
        if approve_form.is_valid() and evaluate_form.is_valid():
            evaluation.evaluation_status = approve_form.cleaned_data['status']
            evaluate_form.save()
            evaluation.save()
            # calc_total_score(evaluation)
            return redirect(reverse_lazy('dashboard'))
