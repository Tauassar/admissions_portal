import logging

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

        evaluations = CandidateEvaluationModel.objects.filter(
            candidate=instance)
        application_eval = [
            ApplicationEvaluationModel(
                evaluation=evaluation
            ) for evaluation in evaluations
        ]
        interview_eval = [
            InterviewEvaluationModel(
                evaluation=evaluation
            ) for evaluation in evaluations
        ]
        InterviewEvaluationModel.objects.bulk_create(interview_eval)
        ApplicationEvaluationModel.objects.bulk_create(application_eval)


'''
    check if evaluation is finished or not
'''


def evaluation_finished_check(sender, instance, created, **kwargs):
    if not created:
        candidate = instance.candidate
        evaluations = candidate.candidateevaluationmodel_set.all()
        # calculate_total_score(evaluations)
        non_approved_evaluations = evaluations.exclude(
            evaluation_status=CandidateEvaluationModel.approved)
        logger.debug(len(non_approved_evaluations))
        if len(non_approved_evaluations) == 0:
            candidate.evaluation_finished = True
            candidate.total_score = calculate_total_score(evaluations)
            candidate.save()


# CONNECTIONS
# post_save.connect(create_sub_evaluations, sender=CandidateEvaluationModel)
post_save.connect(evaluation_finished_check, sender=CandidateEvaluationModel)
post_save.connect(create_candidate_evaluations, sender=CandidateModel)
