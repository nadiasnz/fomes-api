from django.db import models
from django.contrib.auth.models import AbstractUser

class FomesUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    def __str__(self):
        return self.username

class Home(models.Model):
    user = models.ForeignKey(FomesUser, on_delete=models.CASCADE, related_name='homes')
    address = models.CharField(max_length=1000)
    number = models.CharField(max_length=5)
    floor = models.CharField(max_length=5, null=True, blank=True)
    zip_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address} #{self.number}, {self.city}"

class Review(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(FomesUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    description = models.CharField(max_length=1000)
    noise_level = models.IntegerField()
    disturbance_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.home}"
