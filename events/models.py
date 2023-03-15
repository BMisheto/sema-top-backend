from django.db import models
from users.models import *


class Event(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    description = models.TextField()
    start_date = models.CharField(max_length=100,null=True)
    end_date = models.CharField(max_length=100, null=True)
    venue = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    event_cover = models.ImageField(null=True,blank = True,default = "event.jpg",upload_to="event_photos")
    _id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self):
        return str(self._id) + " | " + self.name

        
class Attendee(models.Model):
    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self):
        return str(self._id) + " | " + self.user.email