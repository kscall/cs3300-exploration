from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys

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
        sleep(2)

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
        
        self.selenium.get(self.live_server_url)
        sleep(2)

        signin_link = self.selenium.find_element(By.LINK_TEXT, 'Sign In')
        signin_link.click()

        username_field = self.selenium.find_element(By.XPATH, "//table//input[@name='username']")
        password_field = self.selenium.find_element(By.XPATH, "//table//input[@name='password']")
        loginBtn =  self.selenium.find_element(By.ID, 'loginBtn')

        username_field.send_keys('bob')
        password_field.send_keys('bobbybrown1')
        loginBtn.click()
        sleep(2)

        reviews_link = self.selenium.find_element(By.LINK_TEXT, 'Reviews')
        reviews_link.click()
        sleep(2)
        
        createBtn = self.selenium.find_element(By.ID, 'reviewBtn')
        createBtn.click()
        sleep(2)

        name_field = self.selenium.find_element(By.XPATH, "//table//input[@name='name']")
        name_field.send_keys('Grapes')
        sleep(2)

        details_field = self.selenium.find_element(By.XPATH, "//table//*[@name='details']")
        details_field.send_keys('Absolutely disgusting!')
        sleep(2)

        submitBtn = self.selenium.find_element(By.ID, 'submitBtn')
        submitBtn.click()
        sleep(2)

        reviews = self.selenium.find_elements(By.CLASS_NAME, 'row')
        self.assertNotEqual(len(reviews), 0)







        
