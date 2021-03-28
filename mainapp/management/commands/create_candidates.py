import os

import names
from django.core.files import File
from django.core.management.base import BaseCommand

from auth_app.models import CustomUserModel
from candidates_app.models import CandidateModel, MASTER
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
                diploma=fp
            ) for _ in range(40)]
            candidates = CandidateModel.objects.all()
            CandidateModel.objects.bulk_create(objs)
            objs = [CandidateEvaluationModel(
                candidate=candidate,
                evaluator=evaluator
            ) for candidate in candidates]
            CandidateEvaluationModel.objects.bulk_create(objs)
