
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import *
from users.models import *
from users.serializers import *



# Choice Serializers
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


# Post serializers
class PostsSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True,read_only=True)
    user = UserSmallDetailSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = "__all__"
        
    
    def get_likes(self,obj):
        likes = obj.like_set.all().count()
        return likes
    
    
    


# Comment Serializers
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"



#Comment Likes Serializers
class CommentLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_Like
        fields = "__all__"

