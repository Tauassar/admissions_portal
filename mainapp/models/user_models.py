import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from mainapp.managers import CustomUserManager

class CustomUserModel(AbstractUser):
    """
    User profile model, for managing staff accounts
    """
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
    username = None
    email = models.EmailField(_('email address'), unique=True)
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
