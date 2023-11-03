from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ReviewForm
from django.contrib import messages

# Create your views here.
def index(request):
   

# Render the HTML template index.html with the data in the context variable.
   return render(request, 'food_app/index.html')

class ReviewListView(generic.ListView):
   model = Review
class ReviewDetailView(generic.DetailView):
   model = Review

# Update Review
def createReview(request):
    
    form = ReviewForm()

    if request.method == 'POST':
        
        food_data = request.POST.copy()
        form = ReviewForm(food_data, request.FILES)
        
        if form.is_valid(): 
            form.save()
            return redirect('reviews')
        
    context = {'form': form}
    return render(request, 'food_app/review_form.html', context)

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
      form = ReviewForm(request.POST, instance = review)

      # Ensure updated review credentials are valid
      if form.is_valid():
           
         # If so, update the review
         review.save()

         # Redirect back to the reviews page
         return redirect('reviews')


    context = {'form': form}
    return render(request, 'food_app/review_form.html', context)