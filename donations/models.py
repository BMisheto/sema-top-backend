from django.db import models
from users.models  import *



class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    target = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    donation_cover = models.ImageField(null=True,blank = True,default = "event.jpg",upload_to="donation_photos")
    _id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self):
        return str(self._id) + " | " + self.name 


class Donator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    _id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self):
        return str(self._id) + " | " + self.amount
    