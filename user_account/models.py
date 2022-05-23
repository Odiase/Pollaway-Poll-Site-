from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from PIL import Image
from django.conf import settings
import uuid
from pathlib import Path

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name = "my_profile")
    image = ResizedImageField(size = [300,210],upload_to = "profile_images",force_format = "jpeg",quality = 100,default = f"{settings.BASE_DIR}/media/profile_images/default-image.jpg",blank = True, null = True)
    about = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.user.username} profile"
    

class Followers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    my_followers = models.ManyToManyField(User,related_name = "my_followers")

    def __str__(self):
        return f"{self.user.username} followers"