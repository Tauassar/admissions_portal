import logging

from django.db.models.signals import post_save, pre_delete

from actions_api.models import Action
from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel
from evaluations_app.models import CandidateEvaluationModel

logger = logging.getLogger(__name__)


def admissions_add(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(
            user=instance.created_by,
            name="{0} {1}".format(
                instance.first_name,
                instance.last_name),
            action_type=Action.ADDED
        )
        logger.debug("{0} added new candidate".format(instance.created_by))
    else:
        if instance.last_updated_by.position == \
                CustomUserModel.ADMISSION_DEPARTMENT:
            Action.objects.create(
                user=instance.created_by,
                name="{0} {1}".format(
                    instance.first_name,
                    instance.last_name),
                action_type=Action.EDITED)
            logger.debug("{0} edited candidate".format(instance.created_by))


def admissions_remove(sender, instance, *args, **kwargs):
    if instance.created_by:
        Action.objects.create(
            user=instance.created_by,
            name="{0} {1}".format(
                instance.first_name,
                instance.last_name),
            action_type=Action.DELETED)
        logger.debug("{0} deleted new candidate".format(instance.created_by))


def committie_evaluated(sender, instance, *args, **kwargs):
    if instance.evaluation_status in [CandidateEvaluationModel.in_progress]:
        Action.objects.create(
            user=instance.evaluator,
            name="{0} {1}".format(
                instance.candidate.first_name,
                instance.candidate.last_name),
            action_type=Action.EDITED)
        logger.debug("{0} edited evaluation".format(instance.evaluator))


def secretary_checked(sender, instance, *args, **kwargs):
    if instance.last_updated_by.position == CustomUserModel.SECRETARY:
        if instance.evaluation_status in [CandidateEvaluationModel.approved,
                                          CandidateEvaluationModel.rejected]:
            Action.objects.create(
                user=instance.last_updated_by,
                name="{0} {1}".format(
                    instance.candidate.first_name,
                    instance.candidate.last_name),
                action_type=Action.APPROVED if
                instance.evaluation_status == CandidateEvaluationModel.approved
                else Action.REJECTED)
            logger.debug("{0} rejected evaluation".format(
                instance.last_updated_by))


post_save.connect(admissions_add, sender=CandidateModel)
post_save.connect(committie_evaluated, sender=CandidateEvaluationModel)
post_save.connect(secretary_checked, sender=CandidateEvaluationModel)
pre_delete.connect(admissions_remove, sender=CandidateModel)
