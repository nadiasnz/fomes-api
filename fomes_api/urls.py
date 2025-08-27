from django.urls import path
from .views import (
    RegisterView, ChangePasswordView, 
    CreateHomeAndReviewView, HomesWithUserReviewsView, ReviewViewSet, HomesView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reviews:create_with_home/', CreateHomeAndReviewView.as_view(), name='reviews'),
    path('reviews:user/', HomesWithUserReviewsView.as_view(), name='reviews-user'),
    path('homes/', HomesView.as_view(), name='homes'),
]
