from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import (
    CandidateModel,
    CandidateEvaluationModel,
    CustomUserModel,
    AdmissionRoundModel,
    AdmissionYearModel,
    StaffListModel,
    ApplicationEvaluationModel,
    InterviewEvaluationModel
    )

def candidate_evaluation(sender, instance, created, **kwargs):
    if created:
        evaluators = CustomUserModel.objects.filter(position__in = [1, 2])
        for person in evaluators:
                CandidateEvaluationModel.objects.create(
                evaluator = person,
                candidate = instance
            )

def create_profile(sender, instance, created, **kwargs):
    if created:        
        CustomUserModel.objects.create(user = instance)

'''
    Set old admission years to inactive when new admission year is created
'''
def create_admission_year(sender, instance, created, **kwargs):
    if created:
        AdmissionRoundModel.objects.create(admission_year = instance, round_number=1)
        StaffListModel.objects.create(admission_year = instance)

        active_years = AdmissionYearModel.objects.filter(active =True).exclude(id=instance.id)
        for year in active_years:
            year.active = False
            year.save()
'''
    set old admission periods to false when new period is created
'''
def create_admission_round(sender, instance, created, **kwargs):
    if created:
        active_rounds = AdmissionRoundModel.objects.filter(finished = False).exclude(id=instance.id)
        for subject in active_rounds:
            subject.finished = True
            subject.save()

'''
    set new candidates admission period to current
'''
def create_candidate(sender, instance, **kwargs):
    current_admission_year = AdmissionYearModel.objects.get(active=True)
    current_admission_round = current_admission_year.admissionroundmodel_set.filter(finished=False)
    instance.admission_round = current_admission_round[0]

'''
    Create dependant models for evaluationmodel
'''
def create_evaluations(sender, instance, created, **kwargs):
    if created:
        application_evaluation = ApplicationEvaluationModel.objects.create(
            evaluation=instance)
        interview_evaluation = InterviewEvaluationModel.objects.create(
            evaluation=instance)
'''
    check if evaluation is finished or not
'''
def evaluation_finished_check(sender, instance, **kwargs):
    candidate = instance.candidate
    non_approved_evaluations = candidate.candidateevaluationmodel_set.exclude(evaluation_status=CandidateEvaluationModel.approved)
    if len(non_approved_evaluations)==0:
        candidate.evaluation_finished = True
        candidate.save()

# CONNECTIONS
pre_save.connect(create_candidate, sender=CandidateModel)
post_save.connect(create_evaluations, sender=CandidateEvaluationModel)
post_save.connect(evaluation_finished_check, sender=CandidateEvaluationModel)
post_save.connect(create_profile, sender=User)
post_save.connect(create_admission_year, sender=AdmissionYearModel)
post_save.connect(create_admission_round, sender=AdmissionRoundModel)
post_save.connect(candidate_evaluation, sender=CandidateModel)
