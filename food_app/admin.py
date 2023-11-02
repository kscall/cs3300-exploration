from django.contrib import admin
from .models import Review
from star_ratings.models import Rating

# Register your models here so they can be edited in admin panel
admin.site.register(Review)