from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import (CandidateModel, CandidateEvaluationModel, 
    ProfileModel,AdmissionRoundModel, AdmissionYearModel, StaffListModel)

def candidate_evaluation(sender, instance, created, **kwargs):
    if created:
        evaluators = ProfileModel.objects.filter(position__in = [1, 2])
        
        for person in evaluators:
                CandidateEvaluationModel.objects.create(
                evaluator = person,
                candidate = instance
            )

def create_profile(sender, instance, created, **kwargs):
    if created:        
        ProfileModel.objects.create(user = instance)

def create_admission_year(sender, instance, created, **kwargs):
    if created:
        AdmissionRoundModel.objects.create(admission_year = instance, round_number=1)
        StaffListModel.objects.create(admission_year = instance)

        active_years = AdmissionYearModel.objects.filter(active =True).exclude(id=instance.id)
        for year in active_years:
            year.active = False
            year.save()

def create_admission_round(sender, instance, created, **kwargs):
    if created:
        active_rounds = AdmissionRoundModel.objects.filter(finished = False).exclude(id=instance.id)
        for subject in active_rounds:
            subject.finished = True
            subject.save()

def create_candidate(sender, instance, **kwargs):
    current_admission_year = AdmissionYearModel.objects.get(active=True)
    current_admission_round = current_admission_year.admissionroundmodel_set.filter(finished=False)
    instance.admission_round = current_admission_round[0];


# CONNECTIONS
pre_save.connect(create_candidate, sender=CandidateModel)
post_save.connect(create_profile, sender=User)
post_save.connect(create_admission_year, sender=AdmissionYearModel)
post_save.connect(create_admission_round, sender=AdmissionRoundModel)
post_save.connect(candidate_evaluation, sender=CandidateModel)
