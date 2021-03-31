import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from evaluations_app.models import (CandidateEvaluationModel,
                                    ApplicationEvaluationModel,
                                    InterviewEvaluationModel)
from .utils import calculate_total_score


logger = logging.getLogger(__name__)


def create_candidate_evaluations(sender, instance, created, **kwargs):
    if created:
        evaluators = CustomUserModel.objects.filter(position__in=[1, 2])
        evaluations = [
            CandidateEvaluationModel(
                evaluator=person,
                candidate=instance
            ) for person in evaluators
        ]
        CandidateEvaluationModel.objects.bulk_create(evaluations)


'''
    Create dependant models for evaluation model
'''


def create_sub_evaluations(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, 'interview_evaluation'):
            pass
        else:
            InterviewEvaluationModel.objects.create(
                evaluation=instance)
        if hasattr(instance, 'application_evaluation'):
            pass
        else:
            ApplicationEvaluationModel.objects.create(
                evaluation=instance)


'''
    check if evaluation is finished or not
'''


def evaluation_finished_check(sender, instance, created, **kwargs):
    if not created:
        candidate = instance.candidate
        evaluations = candidate.candidateevaluationmodel_set.all()
        calculate_total_score(evaluations)
        non_approved_evaluations = evaluations.exclude(
            evaluation_status=CandidateEvaluationModel.approved)
        if len(non_approved_evaluations) == 0:
            candidate.evaluation_finished = True
            candidate.total_score = calculate_total_score(evaluations)
            candidate.save()


# CONNECTIONS
post_save.connect(create_sub_evaluations, sender=CandidateEvaluationModel)
post_save.connect(evaluation_finished_check, sender=CandidateEvaluationModel)
post_save.connect(create_candidate_evaluations, sender=CandidateModel)
