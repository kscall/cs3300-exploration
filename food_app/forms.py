from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Class for review form
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'rating', 'details', 'image')

# Class for create user form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Class for profile form
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'name', 'email', 'biography']