# Django Import 
from django.urls import reverse
from http.client import HTTPResponse
from urllib import response
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.hashers import make_password

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics,status,response

from django.core.mail import send_mail

from django.conf import settings

# Rest Framework Import
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

# Rest Framework JWT 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Local Import 
from .models import *
from . import *

from django.utils.encoding import force_bytes
from .serializers import UserSerializerWithToken,UserSerializer,EmailSerializer,ResetPasswordSerializer





# JWT Views
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
       
        serializer = UserSerializerWithToken(self.user).data

        for k,v in serializer.items():
            data[k] =v

        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['message'] = "Hello!"
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# SHOP API
@api_view(['GET'])
def getRoutes(request):
    routes =[
        '/products/',
        '/products/<id>',
        '/users',
        '/users/register',
        '/users/login',
        '/users/profile',
        '/users/forget-password',
    ]
    return Response(routes)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            mobile = data['mobile'],
            email = data['email'],
            password = make_password(data['password']),
        )

        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    
    except:
        message = {"detail":"User with this email is already registered"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user =request.user 
    serializer = UserSerializer(user,many = False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user =request.user 
    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.mobile = data['mobile']
    user.email = data['email']
    user.country = data['country']
    user.bio = data['bio']
    user.company = data['company']
   
    user.save()
    serializer = UserSerializerWithToken(user,many = False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    query = request.query_params.get("keyword")
    if query == None:
        query =''
    lookup = Q( email__icontains=query)  | Q(id__icontains=query) 
    users = User.objects.filter(lookup).order_by('-id')
    users_count =  User.objects.all().count()
    page = request.query_params.get('page')
    paginator = Paginator(users, 2)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)

    serializer = UserSerializer(users,many = True)
    return Response({'users': serializer.data, "count": users_count ,'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users,many = False)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request,pk):
    user =User.objects.get(id=pk)
    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.mobile = data['mobile']
    user.bio = data['bio']
    user.company = data['company']
   
    
    user.save()
    serializer = UserSerializer(user,many = False)
    return Response({"user":serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def makeUserAdmin(request):
    try:
        user_id = int(request.data['user'])
        user = User.objects.get(id=user_id)
    except (KeyError, ValueError, TypeError, User.DoesNotExist):
        return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

    if user.is_staff:
        user.is_staff = False
    else:
        user.is_staff = True
    user.save()

    serializer = UserSerializer(user)
    return Response({"user": serializer.data})





  
   
    
    user.save()
    serializer = UserSerializer(user,many = False)
    return Response({"user":serializer.data})


@api_view(['POST'])
def uploadProfileImage(request):
    data = request.data
    user_id = data['user_id']
    user = User.objects.get(id=user_id)
    user.profile_photo = request.FILES.get('image')
    user.save()
    return Response("Profile photo updated")






@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request,pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response("User was deleted")




    
# //password reset

class PasswordResetRequest(generics.GenericAPIView):

    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token  = PasswordResetTokenGenerator().make_token(user)

            reset_url = reverse(
                "reset_password",
                kwargs = {"encoded_pk":encoded_pk, "token" :token}
            )
            reset_url = f"{settings.FRONTEND_URL}{reset_url}"
            message = f"Your password reset Link, {settings.FRONTEND_URL}{reset_url}";
            subject = 'Password Reset'
            email_from = settings.EMAIL_HOST_USER
            to =[email]
            # send_mail( subject, message, email_from, to)
            # print(send_mail)
            return response.Response(
                {
                    "message": f"Your reset link: {reset_url}"

                },
                status=status.HTTP_200_OK
            )

        else:
            return response.Response(
                { "message" : "User does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )




class ResetPassword(generics.GenericAPIView):

    serializer_class= ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"kwargs":kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return response.Response(
            {"message" : "Password Reset Complete"},
            status=status.HTTP_200_OK
        )
