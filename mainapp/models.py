from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    position = models.TextField()

    def __str__(self):
        return self.first_name+" "+self.last_name


class PortfolioModel(models.Model):
    
    first_name = models.TextField()
    last_name = models.TextField()
    gpa = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name+" "+self.last_name


class EvaluationModel(models.Model):
    portfolio = models.OneToOneField(PortfolioModel, on_delete=models.CASCADE, default=None)
    portfolioEval = models.IntegerField()
    oralEval = models.IntegerField()