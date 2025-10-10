from django.db import models
from django.contrib.auth.models import AbstractUser

# This is our user database table, which is based on django user 
class FomesUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)


class Home(models.Model):
    user = models.ForeignKey(
        FomesUser, on_delete=models.CASCADE, related_name='homes',
        help_text='The user that created the home'
    )
    address = models.CharField(max_length=1000)
    number = models.CharField(max_length=5)
    floor = models.CharField(max_length=5, null=True, blank=True)
    zip_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    home = models.ForeignKey(
        Home, on_delete=models.CASCADE, related_name='reviews',
        help_text='The home which the review is about'
    )
    user = models.ForeignKey(
        FomesUser, on_delete=models.CASCADE, related_name='reviews',
        help_text='The user that created the review'
    )
    rating = models.IntegerField()
    description = models.CharField(max_length=1000)
    noise_level = models.IntegerField()
    disturbance_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
