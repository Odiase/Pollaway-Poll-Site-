from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Settings(models.Model):
    user = models.OneToOneField(User, models.CASCADE,related_name="settings")
    hide_profile = models.BooleanField(default = False,blank = True)
    dark_theme = models.BooleanField(default = False,blank = True)
    turn_on_email_notifications = models.BooleanField(default = False,blank = True)
    allow_followers = models.BooleanField(default = True,blank = True)
    hide_subscribers = models.BooleanField(default = False,blank = True)

    def __str__(self):
        return f"{self.user.username} settings"