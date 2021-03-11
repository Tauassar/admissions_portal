import datetime
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from mainapp.fields import MinMaxInt
from .user_models import CustomUserModel

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

    def __str__(self):
        return "{0} {1}".format(self.list_type, str(self.id))



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
    current_candidates = models.OneToOneField(
        StudentList, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return "Admissions year: {0}-{1}".format(str(self.start_year), str(self.end_year))

    def get_current_admission_round(self):
        try:
            output=self.admissionroundmodel_set.get(finished=False)
            return output
        except Exception as e:
            print(e)

    def getStaffList(self):
        return self.stafflistmodel

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

def get_current_admission_round():
    try:
        admission_year = AdmissionYearModel.objects.get(active=True)
        admission_round = admission_year.get_current_admission_round()
    except Exception as e:
        print(e)
    return admission_round

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
    accepted_candidates_list = models.OneToOneField(
        StudentList, blank=True, null=True, on_delete=models.PROTECT, related_name="accepted_list")
    rejected_candidates_list = models.OneToOneField(
        StudentList, blank=True, null=True, on_delete=models.PROTECT, related_name="rejected_list")
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
