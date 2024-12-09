from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile and set is_new to True
        UserProfile.objects.create(user=instance, is_new=True)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the UserProfile if it exists
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
