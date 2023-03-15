from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator
from users.models import *


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    link = models.TextField(null=True,blank=True)
    is_poll = models.BooleanField(default=False)
    has_photo = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    postImage = models.ImageField(null=True,blank = True,default = "cover.jpg",upload_to="post_photos")
    _id = models.AutoField(primary_key=True,editable=False)


    def __str__(self):
        return str(self._id) + " | " + self.title



class Choice(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    _id = models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return str(self._id) + " | " + self.choice_text 





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return str(self._id) + " | " + self.content
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True,editable=False)


class Comment_Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True,editable=False)







