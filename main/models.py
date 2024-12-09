from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_growth = models.FloatField(default=0)  # Track business growth (e.g., total sales)
    earnings = models.FloatField(default=0)  # Track total earnings
    referrals = models.IntegerField(default=0)  # Track number of direct referrals
    achievements = models.TextField(blank=True, null=True)  # Track user's achievements
    target = models.FloatField(default=5000)  # Target amount for business growth
    is_retired = models.BooleanField(default=False)  # Track retirement status
    pancard_image = models.ImageField(upload_to='pancards/', null=True, blank=True)  # Track PAN card image
    is_new = models.BooleanField(default=True)  # New user flag

    def __str__(self):
        return self.user.username

