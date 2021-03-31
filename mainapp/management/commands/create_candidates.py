import datetime
import os
import random

import names
from django.core.files import File
from django.core.management.base import BaseCommand

from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel, MASTER, CandidateEducationModel, CandidateTestsModel
from evaluations_app.models import CandidateEvaluationModel


class Command(BaseCommand):
    help = 'Creates candidates'

    def handle(self, *args, **kwargs):
        print(os.getcwd())

        with File(open("static/xlsx/application_template.xlsx", "rb")) as fp:
            evaluator = CustomUserModel.objects.get(email='admin@admin.com')
            objs = [CandidateModel(
                created_by=evaluator,
                first_name=names.get_first_name(),
                last_name=names.get_last_name(),
                applying_degree=MASTER,
                diploma=fp,
                total_score=random.randint(15, 99),
                evaluation_finished=True
            ) for _ in range(40)]
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
            objs1 = [CandidateEvaluationModel(
                candidate=candidate,
                evaluator=evaluator
            ) for candidate in candidates]
            CandidateEvaluationModel.objects.bulk_create(objs1)
