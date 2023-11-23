from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

'''
Unit Tests
'''
class ProfileTestCase(TestCase):
    
    def test_createProfile(self):

        user_data = {
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password1': 'bobbybrown1',
            'password2': 'bobbybrown1',
        }

        response = self.client.post(reverse('register'), data=user_data)

        # Check if the user was created successfully
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='bob').exists())

        created_profile = Profile.objects.get(user__username='bob')
        self.assertEqual(created_profile.email, 'bob@gmail.com')


class LoginTestCase(TestCase):
    
    def test_loginProfile(self):

        user = User.objects.create_user(username='bob', password='bobbybrown1', email='bob@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'bob',
            'password': 'bobbybrown1',
        }

        response = self.client.post(reverse('login'), data=login_data, follow=True)

        # Check if the login was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is now authenticated
        self.assertTrue(self.client.session['_auth_user_id'])

class LogOutTestCase(TestCase):
    
    def test_logoutProfile(self):

        user = User.objects.create_user(username='bob', password='bobbybrown1', email='bob@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'bob',
            'password': 'bobbybrown1',
        }

        self.client.post(reverse('login'), data=login_data, follow=True)

        response = self.client.get(reverse('logout'), follow=True)

        # Check if the logout was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is now unauthenticated
        self.assertFalse(self.client.session.get('_auth_user_id'))

'''
Selenium
'''
class HomePageTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome() 
        super(HomePageTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(HomePageTestCase, self).tearDown()

    def test_HomePageContents(self):

        self.selenium.get(self.live_server_url)

        # Check contents of home page
        header_text = self.selenium.find_element(By.CSS_SELECTOR, '.header h1').text
        self.assertEqual(header_text, "TasteBuds")

        sub_text = self.selenium.find_element(By.CSS_SELECTOR, '.header h2').text
        self.assertEqual(sub_text, "Click 'Reviews' to get started!")


class ReviewTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(ReviewTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ReviewTestCase, self).tearDown()

    def test_ReviewExists(self):
        
        user = User.objects.create_user(username='bob', password='bobbybrown1', email='bob@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'bob',
            'password': 'bobbybrown1',
        }
        
        self.client.post(reverse('login'), data=login_data, follow=True)
        sleep(3)

        review_data = {
            'name': 'Cookie',
            'rating': 5,
            'details': 'Absolutely scrumptious!',
        }

        self.client.post(reverse('create-review'), data=review_data, follow=True)
        sleep(3)

        # Check if review was created
        self.selenium.get(self.live_server_url)
        sleep(10)
        reviews_link = self.selenium.find_element(By.LINK_TEXT, 'Reviews')
        reviews_link.click()

        reviews = self.selenium.find_elements(By.CLASS_NAME, 'row')
        sleep(10)

        # Assert tat reviews exist
        self.assertNotEqual(len(reviews), 0)