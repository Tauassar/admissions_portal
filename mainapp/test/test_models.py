from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from mainapp.models import *


class EntryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            email = 'temporary@gmail.com', password = 'temporary', 
            position = CustomUserModel.committiee_chair)

    def checkStr(self):
        User = get_user_model()
        user = User.objects.get(email = 'temporary@gmail.com')
        self.assertEqual(user.email, 'temporary@gmail.com')

    def checkPosition(self):
        print('check position')
        self.assertEqual(user.position, CustomUserModel.committiee_chair)

    def test_string_representation(self):
        entry = CandidateModel(first_name="Kalimba")
        self.assertEqual(str(entry), entry.first_name+" "+entry.last_name)
