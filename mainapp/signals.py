from django.db.models.signals import post_save, pre_save, post_init
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
    StudentList
    )

def candidate_evaluation(sender, instance, created, **kwargs):
    if created:
        evaluators = CustomUserModel.objects.filter(position__in = [1, 2])
        for person in evaluators:
            CandidateEvaluationModel.objects.create(
                evaluator = person,
                candidate = instance
            )
'''
    Set old admission years to inactive when new admission year is created
'''
def admission_year_created(sender, instance, created, **kwargs):
    if created:
        AdmissionRoundModel.objects.create(admission_year = instance, round_number=1)
        StaffListModel.objects.create(admission_year = instance)
        active_years = AdmissionYearModel.objects.filter(active =True).exclude(id=instance.id)
        for year in active_years:
            year.active = False
            year.save()

def create_waiting_list(sender, created, instance, **kwargs):
    if created:
        instance.current_candidates = StudentList.objects.create(
            list_type = StudentList.WAITING_LIST)
        instance.save()

def create_candidate_lists(sender, created, instance, **kwargs):
    if created:
        print("signal create_candidate_lists initiated")
        instance.accepted_candidates_list = StudentList.objects.create(
            list_type = StudentList.ACCEPTED)
        instance.rejected_candidates_list = StudentList.objects.create(
            list_type = StudentList.REJECTED)
        instance.save()

def admission_round_created(sender, instance, created, **kwargs):
    '''
        set old admission periods to false when new period is created
    '''
    if created:
        active_rounds = AdmissionRoundModel.objects.filter(finished = False).exclude(id=instance.id)
        for subject in active_rounds:
            subject.finished = True
            subject.save()

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
# pre_save.connect(create_candidate, sender=CandidateModel)
post_save.connect(create_waiting_list, sender=AdmissionYearModel)
post_save.connect(create_candidate_lists, sender=AdmissionRoundModel)
post_save.connect(admission_round_created, sender=AdmissionRoundModel)
post_save.connect(create_evaluations, sender=CandidateEvaluationModel)
post_save.connect(evaluation_finished_check, sender=CandidateEvaluationModel)
post_save.connect(admission_year_created, sender=AdmissionYearModel)
post_save.connect(admission_round_created, sender=AdmissionRoundModel)
post_save.connect(candidate_evaluation, sender=CandidateModel)
