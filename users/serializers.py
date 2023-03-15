
from rest_framework import serializers
from http.client import HTTPResponse
from rest_framework.reverse import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    # class Meta:
    #     model = User 
    #     fields = ['_id','id','email','first_name','last_name', 'isAdmin']

    class Meta:
        model = User 
        fields = '__all__'

    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self,obj):
        name = obj.first_name
        if name=="":
            name = obj.email
        return name

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email','first_name','last_name']

 
class UserSmallDetailSerializer(serializers.Serializer):
    class Meta:
        model = User 
        fields = ['email','id','profile_photo','first_name','last_name']


class UserSerializerWithToken(UserSerializer):
    token= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =User
        fields = '__all__'

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ["email"]



class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=4,
    )

    class Meta:
        fields = ("password",)
    
    def validate(self, data):
        password = data.get('password')
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            serializers.ValidationError("Missing Data")
        
        pk= urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
            return response.Response(
            {"message" : "The reset token is invalid"},
        )
        
        user.set_password(password)
        user.save()
        return data