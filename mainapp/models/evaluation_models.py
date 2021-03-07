import uuid
from django.db import models
from mainapp.fields import MinMaxInt,MinMaxFloat
from .candidate_models import CandidateModel
from .user_models import CustomUserModel
from .admission_periods import AdmissionRoundModel, get_current_admission_round

# Class storing evaluation data
class CandidateEvaluationModel(models.Model):
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

    evaluation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    evaluator = models.ForeignKey(CustomUserModel, on_delete = models.CASCADE)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE, default=None)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    admission_round = models.ForeignKey(
        AdmissionRoundModel,
        on_delete=models.CASCADE,
        default=get_current_admission_round)

    evaluation_status = models.CharField(max_length =20, choices=STATUS,default=not_evaluated)
    approved_by_secretary = models.BooleanField(default= False)

    def __str__(self):
        return "{0} {1} ({2} {3})".format(
            self.candidate.first_name,
            self.candidate.last_name,
            self.evaluator.first_name,
            self.evaluator.last_name)


class ApplicationEvaluationModel(models.Model):
    evaluation = models.OneToOneField(
        CandidateEvaluationModel, on_delete=models.CASCADE, related_name='application_evaluation')
    relevancy = MinMaxInt(
        min_value=0,
        max_value=30,
        null=True,
        blank=True,
        verbose_name='Educational Background (relevancy)*')
    statement_of_purpose = MinMaxInt(min_value=0, max_value=7, null=True, blank = True)
    recommendation_1 = MinMaxInt(min_value=0, max_value=5, null=True, blank = True)
    recommendation_2 = MinMaxInt(min_value=0, max_value=5, null=True, blank = True)
    relevant_degrees = MinMaxInt(
        min_value=0,
        max_value=5,
        null=True,
        blank = True,
        verbose_name='Other relevant academic degrees (if any),'    \
        'professional certification, academic distinction')
    evaluation_comment = models.TextField(verbose_name='Comments by Evaluator(mandatory)')

    def get_field(self, field_name):
        return self._meta.get_field(field_name)

    def __str__(self):
        return self.evaluation.candidate.first_name+" "+self.evaluation.candidate.last_name


class InterviewEvaluationModel(models.Model):
    evaluation = models.OneToOneField(CandidateEvaluationModel, on_delete=models.CASCADE)
    work_experience_goals = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank = True,
        verbose_name='Career goals / Professional work experience')
    research_interest_and_motivation = MinMaxInt(min_value=0, max_value=10, null=True, blank = True)
    understanding_of_major = MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Overall understanding of major domain')
    community_involvement =  MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Leadership and Community Involvement')
    interpersonal_skills =  MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Communication and Interpersonal Skills')
    english_level =  MinMaxInt(
        min_value=0,
        max_value=10,
        null=True,
        blank=True,
        verbose_name='Command of English')
    interview_comment = models.TextField(verbose_name='Comments by Evaluator(mandatory)')
    skip_evaluation = models.BooleanField(default=False)

    def __str__(self):
        return self.evaluation.candidate.first_name+" "+self.evaluation.candidate.last_name
