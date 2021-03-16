from django.db import models
from django.db.models.fields.files import FieldFile
from admission_periods_app.models import (
    AdmissionRoundModel,
    StudentList,
)
from admission_periods_app.utils import get_current_admission_round
from candidates_app.utils import file_directory_path
from mainapp.fields import MinMaxInt, MinMaxFloat
from mainapp.models import CreateAndUpdateRoutine

BACHELOR = 0
MASTER = 1
PHD = 2
DEGREE = [
    (BACHELOR, 'BSc'),
    (MASTER, 'MSc'),
    (PHD, 'PhD'),
]

ENROLLED = 0
ACCEPTED = 1
IN_WAITING_LIST = 2
REJECTED = 3
CANDIDATE_STATUS = [
    (ENROLLED, 'Enrolled'),
    (ACCEPTED, 'Accepted for enrollment'),
    (IN_WAITING_LIST, 'In waiting list'),
    (REJECTED, 'Rejected')
]

"""Candidate models to store information about candidate
    and evaluations related to particular candidate"""


class CandidateModel(CreateAndUpdateRoutine):
    # information
    candidate_id = models.AutoField(primary_key=True,
                                    editable=False,
                                    unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    applying_degree = models.IntegerField(choices=DEGREE, default=MASTER)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    admission_round = models.ForeignKey(
        AdmissionRoundModel,
        editable=False,
        default=get_current_admission_round,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    total_score = MinMaxFloat(min_value=0,
                              max_value=100,
                              null=True,
                              blank=True)
    candidate_status = models.IntegerField(blank=True,
                                           null=True,
                                           choices=CANDIDATE_STATUS)
    evaluation_finished = models.BooleanField(default=False)
    # final lists
    student_list = models.ForeignKey(
        StudentList,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='candidates')
    # candidate evaluation
    gpa = MinMaxFloat(min_value=0, max_value=4.0, null=True, blank=True)
    school_rating = MinMaxInt(min_value=0, max_value=5, null=True, blank=True)
    research_experience = MinMaxInt(
        min_value=0,
        max_value=3,
        null=True,
        blank=True,
        verbose_name='Relevant work/research experience')

    # files
    diploma = models.FileField(upload_to=file_directory_path)
    ielts_certificate = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    toefl_certificate = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    english_level_certificate = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    gmat_or_gre = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    statement_of_purpose = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    cv = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    recomendation_1: FieldFile = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)
    recomendation_2 = models.FileField(
        upload_to=file_directory_path, null=True, blank=True)

    # return total score if exists
    def get_score(self):
        if self.total_score is not None:
            return self.total_score
        else:
            return "Evaluation is not finished yet"

    def __str__(self):
        return self.first_name + " " + self.last_name


# Model storing data about candidate tests information
class CandidateTestsModel(CreateAndUpdateRoutine):
    candidate = models.OneToOneField(CandidateModel,
                                     on_delete=models.CASCADE,
                                     related_name="testing_info")
    ielts = MinMaxFloat(min_value=1.0,
                        max_value=9.0,
                        null=True,
                        blank=True,
                        help_text='IELTS')
    toefl = MinMaxInt(min_value=0,
                      max_value=120,
                      null=True,
                      blank=True,
                      help_text='TOEFL')
    gre = MinMaxInt(min_value=0,
                    max_value=340,
                    null=True,
                    blank=True,
                    help_text='GRE')

    def __str__(self):
        return "Test information for {0} {1}".format(
            self.candidate.first_name,
            self.candidate.last_name
        )


# model storing data about candidate education
class CandidateEducationModel(CreateAndUpdateRoutine):
    candidate = models.ForeignKey(
        CandidateModel,
        on_delete=models.CASCADE,
        related_name="education_info")
    start_date = models.DateField()
    end_date = models.DateField()
    grad_date = models.DateField()
    degree_type = models.IntegerField(choices=DEGREE, default=MASTER)
    institution = models.CharField(max_length=255)
    study_field = models.CharField(max_length=255)
    gpa = MinMaxFloat(min_value=0, max_value=4.0, null=True, blank=True)

    def __str__(self):
        return self.candidate.first_name + " " + self.candidate.last_name
