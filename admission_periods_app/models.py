import datetime
import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

from mainapp.fields import MinMaxInt
from auth_app.models import CustomUserModel
from admission_periods_app.utils import (get_current_admission_year,
                                         set_round_number)
from mainapp.models import CreateAndUpdateRoutine


logger = logging.getLogger(__name__)


class StudentList(CreateAndUpdateRoutine):
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


class AdmissionYearModel(CreateAndUpdateRoutine):
    """
    Stores data about particular admission year, changes once a year
    """
    start_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator((datetime.datetime.now().year - 2)),
            MaxValueValidator((datetime.datetime.now().year + 2))],
        default=datetime.datetime.now().year,
        unique=False if settings.DEBUG else True,
        help_text="Use the following format: <YYYY>")
    end_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator((datetime.datetime.now().year - 2)),
            MaxValueValidator((datetime.datetime.now().year + 2))],
        default=datetime.datetime.now().year + 1,
        unique=False if settings.DEBUG else True,
        help_text="Use the following format: <YYYY>")
    active = models.BooleanField(default=True)
    current_candidates = models.OneToOneField(
        StudentList, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return "Admissions year: {0}-{1}".format(
            str(self.start_year), str(self.end_year))

    @property
    def get_current_admission_round(self):
        try:
            return self.rounds.get(finished=False)
        except ObjectDoesNotExist as e:
            logger.warning(e)

    def get_staff_list(self):
        try:
            return self.staff_list.staff
        except ObjectDoesNotExist as e:
            logger.warning(e)


class StaffListModel(CreateAndUpdateRoutine):
    """
    Stores information about staff involved in particular admission year
    """
    admission_year = models.OneToOneField(
        AdmissionYearModel,
        on_delete=models.CASCADE,
        related_name='staff_list')
    staff = models.ManyToManyField(CustomUserModel)

    def __str__(self):
        return "Staff list for year: {0}-{1}".format(
            self.admission_year.start_year,
            self.admission_year.end_year)


class AdmissionRoundModel(CreateAndUpdateRoutine):
    """
    stores information about current admission round
    """
    MAX_ROUNDS = 3
    admission_year = models.ForeignKey(
        AdmissionYearModel,
        default=get_current_admission_year,
        on_delete=models.CASCADE,
        related_name='rounds')
    accepted_candidates_list = models.OneToOneField(
        StudentList,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="accepted_list")
    rejected_candidates_list = models.OneToOneField(
        StudentList,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="rejected_list")
    round_number = MinMaxInt(
        min_value=1, max_value=MAX_ROUNDS, default=set_round_number)
    threshold = MinMaxInt(
        min_value=0, max_value=100, default=None, blank=True, null=True)
    mean_score = models.FloatField(default=None, blank=True, null=True)
    finished = models.BooleanField(default=False)

    def calculate_mean_score(self):
        """
        calculate mean score among all candidates
        of the following admission round
        """
        return self.candidates.all().aggregate(Avg('total_score'))

    def __str__(self):
        return "Round #{0} year: {1}-{2}".format(
            self.round_number,
            self.admission_year.start_year,
            self.admission_year.end_year
        )
