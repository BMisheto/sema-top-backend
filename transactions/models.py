from django.db import models
from users.models import *
from donations.models import *

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    _id = models.AutoField(primary_key=True,editable=False)



