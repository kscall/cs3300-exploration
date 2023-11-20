from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import *

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')
    
    return wrapper_func

def incorrect_author(view_func):
    def wrapper_func(request, *args, **kwargs):
        review_id = kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        if request.user == review.author.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')
    
    return wrapper_func




    
        