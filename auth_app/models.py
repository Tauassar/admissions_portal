import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
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
