import uuid
import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from .fields import MinMaxInt,MinMaxFloat

MASTER = 1
PHD = 2
DEGREE = [
    (MASTER, 'MSc'),
    (PHD, 'PhD'),
]

ENROLLED=0
ACCEPTED=1
IN_WAITING_LIST=2
REJECTED=3
CANDIDATE_STATUS = [
(ENROLLED, 'Enrolled'),
(ACCEPTED, 'Accepted for enrollment'),
(IN_WAITING_LIST, 'In waiting list'),
(REJECTED, 'Rejected')
]

# choices = [
#     (1, '1'),
#     (2, '2'),
#     (3, '3'),
#     (4, '4'),
#     (5, '5'),
# ]
class CustomUserModel(AbstractUser):
    """
    User profile model, for managing staff accounts
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    admission_department=0
    committiee_member=1
    committiee_chair=2
    school_secretary=3

    POSITIONS = [
    (admission_department, 'Admission department'),
    (committiee_member, 'Admission committie member'),
    (committiee_chair, 'Chair of the admission committie'),
    (school_secretary, 'School Secretary')
    ]

    profile_pic = models.ImageField(default = 'default_user-avatar.png',null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    department = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    position = models.IntegerField(choices=POSITIONS, default=admission_department)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

"""
Models for changing the admission periods, including admission rounds and years
"""
class AdmissionYearModel(models.Model):
    """
    Stores data about particular admission year, changes once a year
    """
    start_year = models.PositiveIntegerField(
            validators=[
                MinValueValidator((datetime.datetime.now().year-2)), 
                MaxValueValidator((datetime.datetime.now().year+2))],
            default = datetime.datetime.now().year,
            unique = False if settings.DEBUG else True,
            help_text="Use the following format: <YYYY>")
    end_year = models.PositiveIntegerField(
            validators=[
                MinValueValidator((datetime.datetime.now().year-2)), 
                MaxValueValidator((datetime.datetime.now().year+2))],
            default = datetime.datetime.now().year+1,
            unique = False if settings.DEBUG else True,
            help_text="Use the following format: <YYYY>")
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Admissions year: {0}-{1}".format(str(self.start_year), str(self.end_year))

    def getCurrentAdmissionRound(self):
        try:
            output=self.admissionroundmodel_set.get(finished=False)
            return output
        except Exception as e:
            print(e)

    def getStaffList(self):
        return StaffListModel.objects.get(admission_year=self).staff.all()

class StaffListModel(models.Model):
    """
    Stores information about staff involved in particular admission year
    """
    admission_year = models.OneToOneField(AdmissionYearModel, on_delete=models.CASCADE)
    staff = models.ManyToManyField(CustomUserModel)

    def __str__(self):
        return "Staff list for year: {0}-{1}".format(
            self.admission_year.start_year,
            self.admission_year.end_year)

def get_current_admission_year():
    """
    returns active admission year
    """
    try:
        admission_year = AdmissionYearModel.objects.get(active=True)
    except Exception:
        return
    return admission_year

def set_round_number():
    """
    Sets default value for admission round count
    (i.e. AdmissionRoundModel's round_number)
    """
    try:
        current_round_number = get_current_admission_round().round_number
        if current_round_number == AdmissionRoundModel.max_rounds:
            raise Exception('Number of admissions rounds exceeded its max value')
    except Exception as e:
        print(e)
        return 1
    return current_round_number+1

class AdmissionRoundModel(models.Model):
    """
    stores information about current admission round
    """
    max_rounds = 3
    admission_year = models.ForeignKey(
        AdmissionYearModel, 
        default=get_current_admission_year, 
        on_delete=models.CASCADE)
    round_number = MinMaxInt(min_value=1, max_value=max_rounds, default =set_round_number)
    threshold=MinMaxInt(min_value=0, max_value=100, default=None, blank=True, null=True)
    mean_score = models.FloatField(default=None, blank=True, null=True)
    finished = models.BooleanField(default = False)
    def calculateMeanScore(self):
        """
        calculate mean score among all candidates of the following admission round
        """
        candidates = self.candidatemodel_set.all()
        sum_score = 0
        for candidate in candidates:
            sum_score+=candidate.total_score

        self.mean_score = sum_score/len(candidates)
        self.save()

    def __str__(self):
        return "Round #{0} year: {1}-{2}".format(
            self.round_number,
            self.admission_year.start_year,
            self.admission_year.end_year
            )


class StudentList(models.Model):
    ACCEPTED = 'Accepted_students'
    WAITING_LIST = 'Waiting_List'
    REJECTED = 'Rejected_students'
    LIST_CHOICES = [
    (ACCEPTED, 'Accepted_students'),
    (WAITING_LIST, 'Waiting_List'),
    (REJECTED, 'Rejected_students'),
    ]
    list_type = models.CharField(max_length=30, choices=LIST_CHOICES)
    admission_round = models.OneToOneField(AdmissionRoundModel, on_delete=models.CASCADE)

"""Candidate models to store information about candidate
    and evaluations related to particular candidate"""
def file_directiry_path(instance, filename):
    """
    sets path of the uploaded files of CandidateModel 
    to a folder named using candidate data
    """
    return '{0}_{1}_{2}/{3}'.format(instance.first_name, instance.last_name,
    instance.date_created.strftime('%d_%m_%Y'),filename)

# Returns active admission round
def get_current_admission_round():
    try:
        admission_year = AdmissionYearModel.objects.get(active=True)
        admission_round = admission_year.getCurrentAdmissionRound()
    except Exception as e:
        print(e)
    return admission_round

class CandidateModel(models.Model):
    #information
    candidate_id = models.AutoField(primary_key=True, editable = False, unique=True) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    applying_degree = models.IntegerField(choices=DEGREE, default =MASTER)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    admission_round = models.ForeignKey(
        AdmissionRoundModel,
        editable=False,
        default=get_current_admission_round,
        on_delete=models.CASCADE)
    total_score = MinMaxFloat(min_value=0, max_value=100, null=True, blank=True)
    candidate_status = models.IntegerField(blank = True, null=True, choices=CANDIDATE_STATUS)
    evaluation_finished = models.BooleanField(default=False)
    # final lists
    student_list = models.ForeignKey(
        StudentList, default=None, null=True, blank=True, on_delete=models.CASCADE)
    #candidate evaluation
    gpa = MinMaxFloat(min_value=0, max_value=4.0, null=True, blank=True)
    school_rating = MinMaxInt(min_value=0, max_value=5, null=True, blank=True)
    research_experience = MinMaxInt(
        min_value=0,
        max_value=3,
        null=True,
        blank=True,
        verbose_name='Relevant work/research experience')

    #files
    diploma = models.FileField(upload_to=file_directiry_path)
    ielts_certificate = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    ielts_certificate = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    toefl_certificate = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    english_level_certificate = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    gmat_or_gre = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    statement_of_purpose = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    cv = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    recomendation_1 = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)
    recomendation_2 = models.FileField(
        upload_to=file_directiry_path, null = True, blank = True)

    # push from waiting list to recomended
    def push_to_upward_list(self):
        self.waiting_list = None
        self.recomended_for_admission_list = self.admission_round.recomendedforadmissionlist
        self.save()

    # return total score if exists
    def get_score(self):
        if self.total_score is not None:
            return self.total_score
        else:
            return "Evaluation is not finished yet"

    def __str__(self):
        return self.first_name+" "+self.last_name

# Model storing data about candidate tests information
class CandidateTestingInformationModel(models.Model):
    candidate = models.OneToOneField(CandidateModel, on_delete=models.CASCADE)
    ielts = MinMaxFloat(min_value=1.0, max_value=9.0, null=True, blank = True, help_text='IELTS')
    toefl = MinMaxInt(min_value=0, max_value=120, null=True, blank = True, help_text='TOEFL')
    gre = MinMaxInt(min_value=0, max_value=340, null=True, blank = True, help_text='GRE')

    def __str__(self):
        return "Test infromation for "+self.candidate.first_name+" "+self.candidate.last_name

# model storing data about candidate education
class CandidateEducationModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    grad_date = models.DateField()
    degree_type = models.IntegerField(choices=DEGREE, default =MASTER)
    institution = models.CharField(max_length=255)
    study_field = models.CharField(max_length=255)
    gpa = MinMaxFloat(min_value=0, max_value=4.0, null=True, blank = True)

    def __str__(self):
        return self.candidate.first_name+" "+self.candidate.last_name

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
    evaluation = models.OneToOneField(CandidateEvaluationModel, on_delete=models.CASCADE)
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


"""Model to store information for the support(information) page"""
class InformationModel(models.Model):
    publication_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title