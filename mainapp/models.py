import uuid
import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from .fields import MinMaxInt,MinMaxFloat

DEGREE = [
    (1, 'MSc'),
    (2, 'PhD'),
]

# choices = [
#     (1, '1'),
#     (2, '2'),
#     (3, '3'),
#     (4, '4'),
#     (5, '5'),
# ]

'''User profile model, for managing staff accounts'''
class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    admission_department=0
    committiee_member=1
    committiee_chair=2
    school_secretary=3

    Positions = [
    (admission_department, 'Admission department'),
    (committiee_member, 'Admission committie member'),
    (committiee_chair, 'Chair of the admission committie'),
    (school_secretary, 'School Secretary')
    ]

    profile_pic = models.ImageField(default = 'default_user-avatar.png',null=True, blank=True)
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(null=False, blank=False)
    department = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    position = models.IntegerField(choices=Positions, default=admission_department)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

'''Models for changing the admission periods, including admission rounds and years'''
class AdmissionYearModel(models.Model):
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
        return "Admissions year: "+str(self.start_year)+"-"+str(self.end_year)


class StaffListModel(models.Model):
    admission_year = models.OneToOneField(AdmissionYearModel, on_delete=models.CASCADE)
    staff = models.ManyToManyField(CustomUserModel)

    def __str__(self):
        return "Staff list for year: "+str(self.admission_year.start_year)+"-"+str(self.admission_year.end_year)

    
class AdmissionRoundModel(models.Model):
    admission_year = models.ForeignKey(AdmissionYearModel, on_delete=models.CASCADE)
    round_number = MinMaxInt(min_value=1, max_value=3, default =1)
    threshold=MinMaxInt(min_value=0, max_value=100, default=0)
    mean_value = models.FloatField(default=0,blank=True)
    finished = models.BooleanField(default = False)

    def __str__(self):
        return "Round #" + str(self.round_number)+" for year: "+str(self.admission_year.start_year)+"-"+str(self.admission_year.end_year)

'''Candidate models to store information about candidate 
    and evaluations related to particular candidate'''

def file_directiry_path(instance, filename):
    return '{0}_{1}_{2}/{3}'.format(instance.first_name, instance.last_name,
    instance.date_created.strftime('%d_%m_%Y'),filename)

class CandidateModel(models.Model):
    #information
    candidate_id = models.AutoField(primary_key=True, editable = False, unique=True) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    applying_degree = models.IntegerField(choices=DEGREE, default =1)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    admission_round = models.ForeignKey(AdmissionRoundModel, on_delete=models.CASCADE)

    #candidate evaluation
    gpa = MinMaxFloat(min_value=0, max_value=4.0, default=0)
    school_rating = MinMaxInt(min_value=0, max_value=5, default=0)
    research_experience = models.IntegerField(default=0)

    #files
    diploma = models.FileField(upload_to=file_directiry_path)
    ielts_certificate = models.FileField(null = True, blank = True)
    ielts_certificate = models.FileField(null = True, blank = True)
    toefl_certificate = models.FileField(null = True, blank = True)
    english_level_certificate = models.FileField(null = True, blank = True)
    gmat_or_gre = models.FileField(null = True, blank = True)
    statement_of_purpose = models.FileField(null = True, blank = True)
    cv = models.FileField(null = True, blank = True)
    recomendation_1 = models.FileField(null = True, blank = True)
    recomendation_2 = models.FileField(null = True, blank = True)


    def __str__(self):
        return self.first_name+" "+self.last_name


class CandidateTestingInformationModel(models.Model):
    candidate = models.OneToOneField(CandidateModel, on_delete=models.CASCADE)
    ielts = MinMaxFloat(min_value=1.0, max_value=9.0, null=True, help_text='IELTS')
    toefl = MinMaxInt(min_value=0, max_value=120, null=True, help_text='TOEFL')
    gre = MinMaxInt(min_value=0, max_value=340, null=True, help_text='GRE')

    def __str__(self):
        return "Test infromation for "+self.candidate.first_name+" "+self.candidate.last_name  


class CandidateEducationModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    grad_date = models.DateField()
    degree_type = models.IntegerField(choices=DEGREE, default =1)
    institution = models.CharField(max_length=255)
    study_field = models.CharField(max_length=255)
    gpa = MinMaxFloat(min_value=0, max_value=4.0, default=0, help_text='GPA')
   
    def __str__(self):
        return self.candidate.first_name+" "+self.candidate.last_name  


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

    status = models.CharField(max_length =20, choices=STATUS,default=not_evaluated)
    approved_by_secretary = models.BooleanField(default= False)

    def __str__(self):
        return self.candidate.first_name+" "+self.candidate.last_name +"("+self.evaluator.first_name+" "+self.evaluator.last_name+")" 


class ApplicationEvaluationModel(models.Model):
    candidate = models.OneToOneField(CandidateEvaluationModel, on_delete=models.CASCADE)
    relevancy = MinMaxInt(min_value=0, max_value=30, default=0)
    statement_of_purpose = MinMaxInt(min_value=0, max_value=7, default=0)
    recommendation_1 = MinMaxInt(min_value=0, max_value=5, default=0)
    recommendation_2 = MinMaxInt(min_value=0, max_value=5, default=0)
    relevant_degrees = MinMaxInt(min_value=0, max_value=5, default=0)
    evaluation_comment = models.TextField()
       
    def __str__(self):
        return self.candidate.first_name+" "+self.candidate.last_name  


class InterviewEvaluationModel(models.Model):
    candidate = models.OneToOneField(CandidateEvaluationModel, on_delete=models.CASCADE)
    work_experience_goals = MinMaxInt(min_value=0, max_value=10, default=0)
    research_interest_and_motivation = MinMaxInt(min_value=0, max_value=10, default=0)
    understanding_of_major = MinMaxInt(min_value=0, max_value=10, default=0)
    community_involvement =  MinMaxInt(min_value=0, max_value=10, default=0)
    interpersonal_skills =  MinMaxInt(min_value=0, max_value=10, default=0)
    english_level =  MinMaxInt(min_value=0, max_value=10, default=0)
    interview_comment = models.TextField()
    skip_evaluation = models.BooleanField(default=False)
       
    def __str__(self):
        return self.candidate.first_name+" "+self.candidate.last_name  


'''Model to store information for the support(information) page'''
class InformationModel(models.Model):
    publication_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    


