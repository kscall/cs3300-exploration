from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from django.contrib import messages

# Create your views here.
def index(request):
   

# Render the HTML template index.html with the data in the context variable.
   return render( request, 'food_app/index.html')

class ReviewListView(generic.ListView):
   model = Review
class ReviewDetailView(generic.DetailView):
   model = Review