from django.urls import path, include
from . import views
from .decorators import *
from django.contrib.auth import views as auth_views


urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.

    # Home Page URL
    path('', views.index, name='index'),

    # List of Reviews URL
    path('reviews/', views.ReviewListView.as_view(), name= 'reviews'),
    # Review Details URL
    path('review/<int:pk>', views.ReviewDetailView.as_view(), name='review-detail'),

    # URLS to create, delete, and update a review respectively
    path('reviews/create_review/', views.createReview, name='create-review'),
    path('review/<int:review_id>/delete_review/', views.deleteReview, name='delete-review'),
    path('review/<int:review_id>/update_review/', views.updateReview, name='update-review'),

    # User Accounts
    path('accounts/login/', unauthenticated_user(auth_views.LoginView.as_view()), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name = 'register'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('accounts/profile/', views.personalProfile, name = 'profile'),
    path('accounts/update_profile/', views.updateProfile, name = 'update-profile'),
    path('accounts/profile/<int:pk>/', views.userProfile, name = 'profile-detail'),

]
