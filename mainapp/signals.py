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
    InterviewEvaluationModel,
    WaitingList
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
        WaitingList.objects.create(admission_year = instance)
        active_years = AdmissionYearModel.objects.filter(active =True).exclude(id=instance.id)
        for year in active_years:
            year.active = False
            year.save()
'''
    set old admission periods to false when new period is created
'''
def create_admission_round(sender, instance, created, **kwargs):
    if created:
        RecomendedForAdmissionList.objects.create(admission_round = instance)
        RejectedList.objects.create(admission_round = instance)
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
def calculate_total_score(evaluations):
    application_total = 0
    interview_total = 0
    interview_count = 0
    try:
        for evaluation in evaluations:
            application_evaluation = evaluation.applicationevaluationmodel
            interview_evaluation = evaluation.interviewevaluationmodel
            application_total=application_total+get_total_application_score(application_evaluation)
            if not interview_evaluation.skip_evaluation:
                interview_total = interview_total+get_total_interview_score(interview_evaluation)
                interview_count = interview_count+1
        return (application_total/len(evaluations))*0.4+(interview_total/interview_count)*0.6
    except Exception:
        pass

# calculate total score for given evaluation
def get_total_interview_score(model):
    if not model.skip_evaluation:
        total = sum(
            [model.work_experience_goals*2,
            model.research_interest_and_motivation*2,
            model.understanding_of_major*1.5,
            model.community_involvement*1.5,
            model.interpersonal_skills*1.5,
            model.english_level*1.5]
        )
        return total
    else:
        return None

def get_total_application_score(model):
    candidate = model.evaluation.candidate
    gpa = getattr(candidate, 'gpa')
    school_rating = getattr(candidate, 'school_rating')
    research_experience = getattr(candidate, 'research_experience')
    total = sum(
        [model.relevancy,
        model.statement_of_purpose,
        model.recommendation_1,
        model.recommendation_2,
        model.relevant_degrees,
        school_rating,
        gpa*7,
        research_experience*5]
    )
    return total

def evaluation_finished_check(sender, instance, created, **kwargs):
    if not created:
        candidate = instance.candidate
        evaluations = candidate.candidateevaluationmodel_set.all()
        calculate_total_score(evaluations)
        non_approved_evaluations = evaluations.exclude(
            evaluation_status=CandidateEvaluationModel.approved)
        if len(non_approved_evaluations)==0:
            candidate.evaluation_finished = True
            candidate.total_score = calculate_total_score(evaluations)
            candidate.save()

# CONNECTIONS
pre_save.connect(create_candidate, sender=CandidateModel)
post_save.connect(create_evaluations, sender=CandidateEvaluationModel)
post_save.connect(evaluation_finished_check, sender=CandidateEvaluationModel)
post_save.connect(create_profile, sender=User)
post_save.connect(create_admission_year, sender=AdmissionYearModel)
post_save.connect(create_admission_round, sender=AdmissionRoundModel)
post_save.connect(candidate_evaluation, sender=CandidateModel)
