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