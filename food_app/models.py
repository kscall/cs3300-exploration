from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Profile Model
class Profile(models.Model):
    # Fields (user, name, email, image, bio)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='profile_pics')
    biography = models.TextField(blank=True, max_length=200)
    is_private = models.BooleanField(default=False)

    # Define default string to return the name for representing the Model object.
    def __str__(self):
        return self.name

    # Returns the URL to access a particular instance of MyModelName.
    # If you define this method, then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site.
    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])
    
    def username(self):
        return self.user.username

# Review Model
class Review(models.Model):
    # Choice of ratings users can rate a food as (1-5)
    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    # Fields (name, author, rating, details, image)
    name = models.CharField("Food", max_length=200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS, default=0)
    details = models.TextField(max_length=200)
    image = models.ImageField(blank=True, upload_to='review_pics')

    # Define default String to return the name for representing the Model object.
    def __str__(self):
        return self.name

    # Returns the URL to access a particular instance of MyModelName.
    # if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('review-detail', args=[str(self.id)])