from django.urls import path
from .views import RegisterView, ChangePasswordView, CreateHomeAndReviewView, HomesWithUserReviewsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reviews/', CreateHomeAndReviewView.as_view(), name='reviews'),
    path('reviews/user', HomesWithUserReviewsView.as_view(), name='user-reviews'),
]
