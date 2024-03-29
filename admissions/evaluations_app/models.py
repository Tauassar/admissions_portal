import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_currentuser.db.models import CurrentUserField
from simple_history.models import HistoricalRecords

from mainapp.fields import MinMaxInt
from candidates_app.models import CandidateModel
from auth_app.models import CustomUserModel
from admission_periods_app.models import AdmissionRoundModel
from admission_periods_app.utils import get_current_admission_round

# Class storing evaluation data
from mainapp.models import CreateAndUpdateRoutine


logger = logging.getLogger(__name__)


class CandidateEvaluationModel(CreateAndUpdateRoutine):
    history = HistoricalRecords(user_model=CustomUserModel)
    not_evaluated = 'Not evaluated'
    in_progress = 'In progress'
    approved = 'Approved'
    rejected = 'Rejected'

    STATUS = [
        (not_evaluated, 'Not evaluated'),
        (in_progress, 'In progress'),
        (approved, 'Approved'),
        (rejected, 'Rejected'),
    ]
    last_updated_by = CurrentUserField(
        on_update=True,
        related_name='updated_by')
    evaluation_id = models.UUIDField(primary_key=True,
                                     default=uuid.uuid4,
                                     editable=False)
    evaluator = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateModel,
                                  on_delete=models.CASCADE,
                                  default=None)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    admission_round = models.ForeignKey(
        AdmissionRoundModel,
        on_delete=models.CASCADE,
        default=get_current_admission_round,
        related_name='evaluations')
    evaluation_status = models.CharField(max_length=20,
                                         choices=STATUS,
                                         default=not_evaluated)

    def __str__(self):
        try:
            return "{0} {1} ({2} {3})".format(
                self.candidate.first_name,
                self.candidate.last_name,
                self.evaluator.first_name,
                self.evaluator.last_name)
        except ObjectDoesNotExist:
            return "evaluation id: {0}({1} {2})".format(
                self.evaluation_id,
                self.evaluator.first_name,
                self.evaluator.last_name
            )


class ApplicationEvaluationModel(CreateAndUpdateRoutine):
    evaluation = models.OneToOneField(
        CandidateEvaluationModel,
        on_delete=models.CASCADE,
        related_name='application_evaluation')
    relevancy = MinMaxInt(
        min_value=0,
        max_value=30,
        null=True,
        blank=True,
        verbose_name='Educational Background (relevancy)*')
    statement_of_purpose = MinMaxInt(min_value=0,
                                     max_value=7,
                                     null=True,
                                     blank=True)
    recommendation_1 = MinMaxInt(min_value=0,
                                 max_value=5,
                                 null=True,
                                 blank=True)
    recommendation_2 = MinMaxInt(min_value=0,
                                 max_value=5,
                                 null=True,
                                 blank=True)
    relevant_degrees = MinMaxInt(
        min_value=0,
        max_value=5,
        null=True,
        blank=True,
        verbose_name='Other relevant academic degrees (if any),'
                     'professional certification, academic distinction')
    evaluation_comment = models.TextField(
        verbose_name='Comments by Evaluator(mandatory)')

    def get_field(self, field_name):
        return self._meta.get_field(field_name)

    def __str__(self):
        return "{0} {1}".format(
            self.evaluation.candidate.first_name,
            self.evaluation.candidate.last_name)


class InterviewEvaluationModel(CreateAndUpdateRoutine):
    evaluation = models.OneToOneField(
        CandidateEvaluationModel,
        on_delete=models.CASCADE,
        related_name='interview_evaluation')
    work_experience_goals = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Career goals / Professional work experience')
    research_interest_and_motivation = MinMaxInt(min_value=0,
                                                 max_value=10,
                                                 null=True,
                                                 blank=True)
    understanding_of_major = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Overall understanding of major domain')
    community_involvement = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Leadership and Community Involvement')
    interpersonal_skills = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Communication and Interpersonal Skills')
    english_level = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Command of English')
    interview_comment = models.TextField(
        verbose_name='Comments by Evaluator(mandatory)')
    skip_evaluation = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(
            self.evaluation.candidate.first_name,
            self.evaluation.candidate.last_name)
