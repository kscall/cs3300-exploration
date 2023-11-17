from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ReviewForm, CreateUserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import *

def index(request):

# Render the HTML template index.html with the data in the context variable.
   return render(request, 'food_app/index.html')

# Review List & Detail View Classes
class ReviewListView(generic.ListView):
   model = Review
class ReviewDetailView(generic.DetailView):
   model = Review

# Create Review
def createReview(request):
    
    # Begin with empty form
    form = ReviewForm()

    if request.method == 'POST':
        
        # Copy user's entered input & uploaded image from form
        food_data = request.POST.copy()
        form = ReviewForm(food_data, request.FILES)
        
        # If user fills out form correctly, create a new review
        if form.is_valid(): 
            form.save()
            # Redirect back to reviews page
            return redirect('reviews')
    
    # Redirect user to create review page
    context = {'form': form}
    return render(request, 'food_app/review_form_create.html', context)

# Delete Review
def deleteReview(request, review_id):
   
    # Initialize review we are deleting
    review = Review.objects.get(pk=review_id)

    # If user confirmed to delete their review, delete it and go back to review page
    if request.method == 'POST':
       
        review.delete()
        return redirect('reviews')


    # Redirect user to page confirming review deletion
    context = {'item': review}
    return render(request, 'food_app/review_delete.html', context)

# Update Review
def updateReview(request, review_id):
   
    # Initialize review we are updating
    review = Review.objects.get(pk=review_id)

    # Create form with preexisting review info
    form = ReviewForm(instance = review)

    if request.method == 'POST':
       
      # Create form instance with submitted data & preexisting review
      form = ReviewForm(request.POST, request.FILES, instance = review)

      # Ensure updated review credentials are valid
      if form.is_valid():
           
         # If so, update the review
         review.save()

         # Redirect back to the review detail page
         return redirect('review-detail', pk=review_id)


    # Redirect user to update review page
    context = {'form': form, 'pk': review_id}
    return render(request, 'food_app/review_form_update.html', context)


#View for registering a user
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method =='POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

        messages.success(request, 'Account was created for ' + username)
        return redirect('login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

'''
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index') 

    context = {}
    return render(request, 'registration/login.html', context)
'''


def logoutUser(request):
    logout(request)
    return redirect('login')

def userProfile(request):
    context = {}
    return render(request, 'registration/profile.html', context)
