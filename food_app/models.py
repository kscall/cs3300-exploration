from django.db import models
from django.urls import reverse


# Create your models here.

class Review(models.Model):

    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    
    name = models.CharField("Food", max_length=200)
    rating = models.IntegerField(choices=RATINGS, default=0)
    details = models.TextField(max_length=200)
    image = models.ImageField(blank=True)
    

    #Define default String to return the name for representing the Model object."
    def __str__(self):
        return self.name


    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('review-detail', args=[str(self.id)])
    