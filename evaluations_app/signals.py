from django.db.models.signals import post_save

from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from evaluations_app.models import (CandidateEvaluationModel,
                                    ApplicationEvaluationModel,
                                    InterviewEvaluationModel)
from .utils import calculate_total_score


def create_candidate_evaluations(sender, instance, created, **kwargs):
    if created:
        evaluators = CustomUserModel.objects.filter(position__in=[1, 2])
        for person in evaluators:
            CandidateEvaluationModel.objects.create(
                evaluator=person,
                candidate=instance
            )


'''
    Create dependant models for evaluation model
'''


def create_sub_evaluations(sender, instance, created, **kwargs):
    if created:
        ApplicationEvaluationModel.objects.create(
            evaluation=instance)
        InterviewEvaluationModel.objects.create(
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
