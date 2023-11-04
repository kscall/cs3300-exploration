from django.forms import ModelForm
from .models import Review


# Create class for review form
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'author', 'rating', 'details', 'image')