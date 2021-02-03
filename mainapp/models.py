import uuid
from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    phone_number = models.IntegerField()
    department = models.TextField()
    school = models.TextField()
    position = models.TextField()

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class PortfolioModel(models.Model):
    choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    candidate_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    first_name = models.TextField()
    last_name = models.TextField()
    gpa = models.IntegerField(default=0, choices=choices)
    school_rating = models.IntegerField(choices=choices)
    recommendations = models.IntegerField(choices=choices)
    educational_backgorund = models.IntegerField(choices=choices)
#    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.first_name+" "+self.last_name


class EvaluationModel(models.Model):
    choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    eval_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    author = models.ManyToManyField(ProfileModel)
    portfolio = models.ForeignKey(PortfolioModel, on_delete=models.CASCADE, default=None)

    gpa = models.IntegerField(default=0, choices=choices)
    school_rating = models.IntegerField(choices=choices)
    recommendations = models.IntegerField(choices=choices)
    educational_backgorund = models.IntegerField(choices=choices)

    understanding_of_major = models.IntegerField(choices=choices)
    research_interest_and_motivation = models.IntegerField(choices=choices)
    experience_and_goals = models.IntegerField(choices=choices)
    english_level = models.IntegerField(choices=choices)


    def __str__(self):
        return self.portfolio.first_name+" "+self.portfolio.last_name

#	date_created = models.DateTimeField(auto_now_add=True, null=True)
