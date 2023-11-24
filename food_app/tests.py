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

# Unit test to create a profile with test data
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

        # Check if user's email matches the email from created profile
        created_profile = Profile.objects.get(user__username='bob')
        self.assertEqual(created_profile.email, 'bob@gmail.com')


# Unit test to log into a profle
class LoginTestCase(TestCase):
    
    def test_loginProfile(self):

        # Create a user and a profile with that user
        user = User.objects.create_user(username='bob', password='bobbybrown1', email='bob@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'bob',
            'password': 'bobbybrown1',
        }

        # Log in
        response = self.client.post(reverse('login'), data=login_data, follow=True)

        # Check if the log in was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is authenticated
        self.assertTrue(self.client.session['_auth_user_id'])

# Unit test to log out of a profile
class LogOutTestCase(TestCase):
    
    def test_logoutProfile(self):

        # Create a user and a profile with that user
        user = User.objects.create_user(username='bob', password='bobbybrown1', email='bob@gmail.com')
        Profile.objects.create(user=user)

        login_data = {
            'username': 'bob',
            'password': 'bobbybrown1',
        }

        self.client.post(reverse('login'), data=login_data, follow=True)

        # Log out
        response = self.client.get(reverse('logout'), follow=True)

        # Check if the log out was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is unauthenticated
        self.assertFalse(self.client.session.get('_auth_user_id'))

'''
Selenium Tests
'''
# Selenium Test to verify user is on home page
class HomePageTestCase(StaticLiveServerTestCase):

    # Function to set up the Chrome Webdriver
    def setUp(self):
        self.selenium = webdriver.Chrome() 
        self.selenium.maximize_window()
        super(HomePageTestCase, self).setUp()

    # Function to tear down the Chrome Webdriver
    def tearDown(self):
        self.selenium.quit()
        super(HomePageTestCase, self).tearDown()

    def test_HomePageContents(self):

        # Go to Home page
        self.selenium.get(self.live_server_url)
        sleep(2)

        # Check contents of home page (headers)
        header_text = self.selenium.find_element(By.CSS_SELECTOR, '.header h1').text
        self.assertEqual(header_text, "TasteBuds")

        sub_text = self.selenium.find_element(By.CSS_SELECTOR, '.header h2').text
        self.assertEqual(sub_text, "Click 'Reviews' to get started!")


# Selenium Test to verify user is on home page
class ReviewTestCase(StaticLiveServerTestCase):

    # Function to set up the Chrome Webdriver
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(ReviewTestCase, self).setUp()

    # Function to tear down the Chrome Webdriver
    def tearDown(self):
        self.selenium.quit()
        super(ReviewTestCase, self).tearDown()

    # Test to confirm whether reviews exist or not
    # Creates a review and compares 1 != 0
    def test_ReviewExists(self):
        
        # Create a user and a profile with that user
        user = User.objects.create_user(username='bob', password='bobbybrown1', email='bob@gmail.com')
        Profile.objects.create(user=user)
        
        # Go to Home page
        self.selenium.get(self.live_server_url)
        sleep(2)

        # Go to Log In page
        login_link = self.selenium.find_element(By.LINK_TEXT, 'Log In')
        login_link.click()

        # Enter account details for log in
        username_field = self.selenium.find_element(By.XPATH, "//table//input[@name='username']")
        password_field = self.selenium.find_element(By.XPATH, "//table//input[@name='password']")
        loginBtn =  self.selenium.find_element(By.ID, 'loginBtn')

        username_field.send_keys('bob')
        password_field.send_keys('bobbybrown1')

        # Log In
        loginBtn.click()

        sleep(2)

        # Go to Reviews Tab
        reviews_link = self.selenium.find_element(By.LINK_TEXT, 'Reviews')
        reviews_link.click()
        sleep(2)
        
        # Click Create a Revew
        createBtn = self.selenium.find_element(By.LINK_TEXT, 'Create a Review')
        createBtn.click()
        sleep(2)

        # Input food name for review
        name_field = self.selenium.find_element(By.XPATH, "//table//input[@name='name']")
        name_field.send_keys('Grapes')
        sleep(2)

        # Leave food rating at default (1)

        # Input food details for revew
        details_field = self.selenium.find_element(By.XPATH, "//table//*[@name='details']")
        details_field.send_keys('Absolutely disgusting!')
        sleep(2)


        # Submit review for creation
        submitBtn = self.selenium.find_element(By.ID, 'submitBtn')
        submitBtn.click()
        sleep(2)

        # Confirm that a review exists by checking if elements exist in the review format class
        reviews = self.selenium.find_elements(By.CLASS_NAME, 'row')
        self.assertNotEqual(len(reviews), 0)







        
