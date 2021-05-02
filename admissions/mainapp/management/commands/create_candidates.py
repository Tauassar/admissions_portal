import datetime
import os
import random

import names
from django.core.files import File
from django.core.management.base import BaseCommand

from admission_periods_app.models import AdmissionYearModel
from auth_app.models import CustomUserModel
from candidates_app.models import (CandidateModel,
                                   MASTER,
                                   CandidateEducationModel,
                                   CandidateTestsModel)
from evaluations_app.models import (CandidateEvaluationModel,
                                    InterviewEvaluationModel,
                                    ApplicationEvaluationModel)


class Command(BaseCommand):
    help = 'Creates candidates'

    def handle(self, *args, **kwargs):
        print(os.getcwd())

        with File(open("static/test_data.pdf", "rb")) as fp:
            evaluator = CustomUserModel.objects.get(email='admin@admin.com')
            objs = [CandidateModel(
                created_by=evaluator,
                first_name=names.get_first_name(),
                last_name=names.get_last_name(),
                applying_degree=MASTER,
                diploma=fp,
                ielts_certificate=fp,
                toefl_certificate=fp,
                english_level_certificate=fp,
                gmat_or_gre=fp,
                statement_of_purpose=fp,
                cv=fp,
                recomendation_1=fp,
                recomendation_2=fp,
                total_score=random.randint(15, 99),
                evaluation_finished=True
            ) for _ in range(20)]
            CandidateModel.objects.bulk_create(objs)
            candidates = CandidateModel.objects.all()

            objs2 = [CandidateEducationModel(
                candidate=candidate,
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now(),
                grad_date=datetime.datetime.now()
            ) for candidate in candidates]
            CandidateEducationModel.objects.bulk_create(objs2)

            objs3 = [CandidateTestsModel(
                candidate=candidate,
            ) for candidate in candidates]
            CandidateTestsModel.objects.bulk_create(objs3)

            create_evaluations(evaluator, candidates)
            staff = \
                CustomUserModel.objects.filter(
                    position=CustomUserModel.COMMITTEE_MEMBER)|\
                CustomUserModel.objects.filter(
                    position=CustomUserModel.COMMITTEE_CHAIR)
            for evaluator in staff:
                create_evaluations(evaluator, candidates)
            evaluations = CandidateEvaluationModel.objects.all()
            interviews = []
            applications = []
            for evaluation in evaluations:
                applications.append(ApplicationEvaluationModel(
                    evaluation=evaluation,
                    relevancy=random.randint(0, 30),
                    statement_of_purpose=random.randint(0, 7),
                    recommendation_1=random.randint(0, 5),
                    recommendation_2=random.randint(0, 5),
                    relevant_degrees=random.randint(0, 5),
                    evaluation_comment='Application test'
                ))
                interviews.append(InterviewEvaluationModel(
                    evaluation=evaluation,
                    work_experience_goals=random.randint(0, 10),
                    research_interest_and_motivation=random.randint(0, 10),
                    understanding_of_major=random.randint(0, 10),
                    community_involvement=random.randint(0, 10),
                    interpersonal_skills=random.randint(0, 10),
                    english_level=random.randint(0, 10),
                    interview_comment='Interview test comment'

                ))
            ApplicationEvaluationModel.objects.bulk_create(applications)
            InterviewEvaluationModel.objects.bulk_create(interviews)


def create_evaluations(evaluator, candidates):
    objs1 = [CandidateEvaluationModel(
        candidate=candidate,
        evaluator=evaluator
    ) for candidate in candidates]

    CandidateEvaluationModel.objects.bulk_create(objs1)