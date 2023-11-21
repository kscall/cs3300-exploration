from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class ProfileTestCase(TestCase):
    
    def test_createProfile(self):

        user_data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        response = self.client.post(reverse('register'), data=user_data)

        # Check if the user was created successfully
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        created_profile = Profile.objects.get(user__username='testuser')
        self.assertEqual(created_profile.email, 'testuser@gmail.com')


class LoginTestCase(TestCase):
    
    def test_loginProfile(self):

        user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('login'), data=login_data, follow=True)

        # Check if the login was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is now authenticated
        self.assertTrue(self.client.session['_auth_user_id'])

class LogOutTestCase(TestCase):
    
    def test_logoutProfile(self):
        user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        self.client.post(reverse('login'), data=login_data, follow=True)

        response = self.client.get(reverse('logout'), follow=True)

        # Check if the logout was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is now unauthenticated
        self.assertFalse(self.client.session.get('_auth_user_id'))


