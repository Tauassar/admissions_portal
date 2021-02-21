from django.test import TestCase

from .models import *


class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = CandidateModel(first_name="Kalimba")
        self.assertEqual(str(entry), entry.first_name+" "+entry.last_name)


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
