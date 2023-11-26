from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import *

# Decorators - called before calling the original function for user authentication

# Decorator handling unauthorized pages for authenticated users
def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # Redirect user to home page
        if request.user.is_authenticated:
            return redirect('index')
        else:
            # Allow user to access content
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


# Decorator handling incorrect author of a review attempting an action
def incorrect_author(view_func):
    def wrapper_func(request, *args, **kwargs):
        # Get the review attempting to be modified
        review_id = kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        # Allow user to modify review if they are the uathor of that review
        if request.user == review.author.user:
            return view_func(request, *args, **kwargs)
        else:
            # Otherwse, redirect them home
            return redirect('reviews')
    
    return wrapper_func

