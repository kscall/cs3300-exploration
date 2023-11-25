from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *

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

# Create Review - user must be logged in to do so
@login_required(login_url='login')
def createReview(request):
    
    # Begin with empty form
    form = ReviewForm()

    if request.method == 'POST':

        # Get the currently logged-in customer
        profile = request.user.profile  
        
        # Copy user's entered input & uploaded image from form
        food_data = request.POST.copy()
        form = ReviewForm(food_data, request.FILES)
        
        # If user fills out form correctly, create a new review
        if form.is_valid(): 

            review = form.save(commit=False)
            review.author = profile
            form.save()

            # Redirect user to their profile with review
            return redirect('profile')
    
    # Redirect user to create review page
    context = {'form': form}
    return render(request, 'food_app/review_form_create.html', context)

# Delete review - ensure users can only delete their own reviews
@incorrect_author
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

# Update review - users can only update their own reviews
@incorrect_author
def updateReview(request, review_id):
   
    # Initialize review we are updating
    review = Review.objects.get(pk=review_id)

    # Create form with preexisting review info
    form = ReviewForm(instance = review)

    # If user confirmed to update their review, update it and go back to review detail page
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


# View for registering a user - logged in users cannot register
@authenticated_user
def registerPage(request):

    # Create form for registering
    form = CreateUserForm()

    # If user confirmed to register, create account and go to log in page
    if request.method =='POST':

        # Create form instance with submitted data
        form = CreateUserForm(request.POST)

        # Ensure account data is valid
        if form.is_valid():

            user = form.save()
            username = form.cleaned_data.get('username')

            # Create a profile based on user credentials
            Profile.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

        messages.success(request, 'Account was created for ' + username)
        return redirect('login')

    # Redirect user to register page
    context = {'form': form}
    return render(request, 'registration/register.html', context)

# Log out the user
def logoutUser(request):
    logout(request)
    return redirect('login')

# View for user's personal profile
@login_required(login_url='login')
def personalProfile(request):
    
    # Send in profile and query of their personal reviews to vew
    profile = request.user.profile 
    review_list = Review.objects.filter(author=profile)
    
    context = {'profile': profile, 'review_list': review_list}

    return render(request, 'registration/profile.html', context)

# View for user's non-personal profile
def userProfile(request, username):

    # Get the user of the profile we are trying to view
    user = get_object_or_404(User, username=username)
    # Send in profile and query of the profile's reviews to view
    profile = get_object_or_404(Profile, user=user)
    review_list = Review.objects.filter(author=profile)

    context = {'profile': profile, 'review_list': review_list, 'user': request.user, 'username': username}
    
    return render(request, 'registration/profile.html', context)


# View for updating a profile - logged out users do not have a profile to modify
@login_required(login_url='login')
def updateProfile(request):

    # Get the user's profile
    profile = request.user.profile

    # Create profile form to modify for corresponding profile
    form = ProfileForm(instance=profile)

    # If user confirmed to update their profile, update it and go back to profile page
    if request.method == 'POST':
    
        # Create profile instance with submitted data
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        # Ensure updated review credentials are valid
        if form.is_valid():
          
            # If so, update the profile
            profile = form.save(commit=False)
            # Determines if profile should be private based on state of switch on form
            profile.is_private = request.POST.get('is_private') == 'on'
            profile.save()

        return redirect('profile')
        
    context = {'form': form}
    return render(request, 'registration/profile_form_update.html', context)


