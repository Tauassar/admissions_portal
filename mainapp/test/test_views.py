from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from mainapp.models import *

class ProjectTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary@gmail.com', 'temporary')
    
    # Login check
    def test_secure_page(self):
        User = get_user_model()
        self.client.login(username='temporary@gmail.com', password='temporary')
        response = self.client.get('/', follow=True)
        user = CustomUserModel.objects.get(email='temporary@gmail.com')
        # dashboard check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].email, 'temporary@gmail.com')
    
    #check redirects
    def test_redirects_for_non_logged_users(self):
        links = ['/info', '/contacts', '/personal']
        for link in links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 301)
        link ='/'
        response = self.client.get(link)
        self.assertEqual(response.status_code, 302)

    #check redirects
    def test_status_codes(self):
        links = ['/', '/info', '/contacts', '/personal']
        for link in links:
            response = self.client.get(link, follow=True)
            self.assertEqual(response.status_code, 200)