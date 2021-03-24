from django.db import models

from auth_app.models import CustomUserModel
from mainapp.models import CreateAndUpdateRoutine

"""
    admission
added
Edited
deleted
    chair
evaluated
edited evaluation
    secretary
approved
rejected approvement
"""


class Action(models.Model):
    # admissions
    ADDED = 'added'
    EDITED = 'edited'
    DELETED = 'deleted'
    # committie
    Evaluated = 'added'
    # secretary
    APPROVED = 'approved'
    REJECTED = 'rejected'
    LIST_CHOICES = [
        (ADDED, 'candidate added'),
        (EDITED, 'candidate edited'),
        (DELETED, 'candidate deleted'),
        (Evaluated, 'candidate evaluated'),
        (APPROVED, 'evaluation approved'),
        (REJECTED, 'evaluation rejected'),
    ]

    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    name = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=30, choices=LIST_CHOICES)

    def __str__(self):
        return "{0} {1}".format(self.name, self.action_type)
