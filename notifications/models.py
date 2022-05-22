from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
    #Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "notifications")
    message = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add = True)
    read = models.BooleanField(default = False)
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique = True,editable=False)
    deleted = models.BooleanField(default = False, null= True, blank = True)
    
    def __str__(self):
        return  f"{self.user.username} notification"
    
    def save(self, *args, **kwargs):
        '''this checks if this instace already exists and updates just the 'read' attribute'''
        if not self.id:
            self.time = timezone.now()
        return super(Notification, self).save(*args, **kwargs) # calling the main save method on this instance