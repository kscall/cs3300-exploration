from django.forms import ModelForm
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create class for review form
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'author', 'rating', 'details', 'image')

# Create class for user form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']