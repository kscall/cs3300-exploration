from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Class for review form
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'rating', 'details', 'image')

        labels = {
            'name': 'Food Name',
        }

# Class for create user form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Class for profile form
class ProfileForm(ModelForm):
    
    username = forms.CharField(disabled=True, required=False)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'name', 'email', 'biography']

        labels = {
            'image': 'Profile Picture',
            'biography': 'About Me',
        }

        # Allow user to see their username, but not modify it
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Set value of 'username' field to the user's username
        if self.instance.user:
            self.initial['username'] = self.instance.user.username