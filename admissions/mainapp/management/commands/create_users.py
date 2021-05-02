import random

import names
from django.core.management.base import BaseCommand

from auth_app.models import CustomUserModel


class Command(BaseCommand):
    help = 'Creates users'

    def handle(self, *args, **kwargs):
        objs = [CustomUserModel(
            email='{0}{1}@email.com'.format(names.get_first_name(), random.randint(0, 30)),
            first_name=names.get_first_name(),
            last_name=names.get_last_name(),
            password='123456987654Yy',
            position=random.randint(0, 3)
        )for e in range(40)]
        CustomUserModel.objects.bulk_create(objs)


