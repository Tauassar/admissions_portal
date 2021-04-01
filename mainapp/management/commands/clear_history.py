from django.core.management import BaseCommand
from simple_history.management.commands import clean_old_history


class Command(BaseCommand):
    help = 'Creates candidates'

    def handle(self, *args, **kwargs):
        clean_old_history()
