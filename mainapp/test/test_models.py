from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

import mainapp.models


class EntryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        user = user.objects.create_user(
            email='temporary@gmail.com', password='temporary',
            position=mainapp.models.CustomUserModel.committiee_chair)

    def checkStr(self):
        User = get_user_model()
        user = User.objects.get(email='temporary@gmail.com')
        self.assertEqual(user.email, 'temporary@gmail.com')

    def checkPosition(self):
        print('check position')
        self.assertEqual(user.position,
                         mainapp.models.CustomUserModel.committiee_chair)

    def test_string_representation(self):
        entry = mainapp.models.CandidateModel(first_name="Kalimba")
        self.assertEqual(str(entry), entry.first_name + " " + entry.last_name)
