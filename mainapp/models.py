import uuid
from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Positions = [
        (0, 'Admission department'),
        (1, 'Admission committie member'),
        (2, 'Chair of the admission committie'),
        (3, 'School Secretary')
    ]

    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    phone_number = models.IntegerField()
    department = models.TextField()
    school = models.TextField()
    position = models.IntegerField(choices=Positions, default=0)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class CandidateModel(models.Model):
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
    date_created = models.DateTimeField(auto_now_add=True, null=True)

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
    STATUS = [
        ('Not evaluated', 'Not evaluated'),
        ('In progress', 'In progress'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    evaluation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    evaluator = models.ForeignKey(ProfileModel, on_delete = models.CASCADE)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE, default=None)

    gpa = models.IntegerField(choices=choices,null = True)
    school_rating = models.IntegerField(choices=choices,null = True),
    recommendations = models.IntegerField(choices=choices,null = True)
    educational_backgorund = models.IntegerField(choices=choices,null = True)

    understanding_of_major = models.IntegerField(choices=choices,null = True)
    research_interest_and_motivation = models.IntegerField(choices=choices,null = True)
    experience_and_goals = models.IntegerField(choices=choices,null = True)
    english_level = models.IntegerField(choices=choices,null = True)
    
    status = models.CharField(max_length =20, choices=STATUS,default='Not evaluated')

    approved_by_secretary = models.BooleanField(default= False)


    def __str__(self):
        return self.candidate.first_name+" "+self.candidate.last_name +"("+self.evaluator.user.first_name+" "+self.evaluator.user.last_name+")" 

#	date_created = models.DateTimeField(auto_now_add=True, null=True)


class InformationModel(models.Model):
    publication_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title = models.TextField()
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

