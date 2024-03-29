import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.admin import SimpleHistoryAdmin
from simple_history.models import HistoricalRecords

from auth_app.managers import CustomUserManager


class CustomUserModel(AbstractUser):
    """
    User profile model, for managing staff accounts
    """
    ADMISSION_DEPARTMENT = 0
    COMMITTEE_MEMBER = 1
    COMMITTEE_CHAIR = 2
    SECRETARY = 3
    POSITIONS = [
        (ADMISSION_DEPARTMENT, 'Admission department'),
        (COMMITTEE_MEMBER, 'Admission committee member'),
        (COMMITTEE_CHAIR, 'Chair of the admission committee'),
        (SECRETARY, 'School Secretary')
    ]
    username = None
    email = models.EmailField(_('email address'), unique=True)
    staff_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    profile_pic = models.ImageField(
        default='default_user-avatar.png', null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    department = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    position = models.IntegerField(
        choices=POSITIONS, default=ADMISSION_DEPARTMENT)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    def __unicode__(self):
        return '{0} IP: {1} at: {2}'.format(
            self.action, self.ip, self.created_at.strftime('%d.%m.%Y %H:%M'))

    def __str__(self):
        return '{0} IP: {1} at: {2}'.format(
            self.action, self.ip, self.created_at.strftime('%d.%m.%Y %H:%M'))
