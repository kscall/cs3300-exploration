from django.urls import path
from . import views


urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
    path('', views.index, name='index'),

    path('reviews/', views.ReviewListView.as_view(), name= 'reviews'),
    path('review/<int:pk>', views.ReviewDetailView.as_view(), name='review-detail'),

    path('reviews/create_review/', views.createReview, name='create-review'),
    path('review/<int:review_id>/delete_review/', views.deleteReview, name='delete-review'),
    path('review/<int:review_id>/update_review/', views.updateReview, name='update-review'),
    
]
