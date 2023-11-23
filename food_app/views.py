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

# Create Review
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
            if review.author.is_private :
                return redirect('profile')
            else:
                return redirect('reviews')
    
    # Redirect user to create review page
    context = {'form': form}
    return render(request, 'food_app/review_form_create.html', context)

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

@incorrect_author
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
            user = form.save()
            username = form.cleaned_data.get('username')

            Profile.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')

def personalProfile(request):
    profile = request.user.profile 
    review_list = Review.objects.filter(author=profile)
    
    context = {'profile': profile, 'review_list': review_list}

    return render(request, 'registration/profile.html', context)

def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    review_list = Review.objects.filter(author=profile)

    context = {'profile': profile, 'review_list': review_list, 'user': request.user, 'username': username}
    
    return render(request, 'registration/profile.html', context)


@authenticated_user
def updateProfile(request):

    profile = request.user.profile

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
    
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
          
            profile = form.save(commit=False)
            profile.is_private = request.POST.get('is_private') == 'on'
            profile.save()

            return redirect('profile')
        
    context = {'form': form}
    return render(request, 'registration/profile_form_update.html', context)


