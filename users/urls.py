from django.urls import path
from .views import *


urlpatterns = [
    path('register/', registerUser,name='register'),
    path('makeadmin/', makeUserAdmin,name='make-admin'),
    path('', getUsers,name="users"),
    path('forget-password/', PasswordResetRequest.as_view(), name="forget_password"),
    path('reset-password/<str:encoded_pk>/<str:token>/', ResetPassword.as_view(), name="reset_password"),
    path('profile/', getUserProfile,name="user_profile"),
    path('profile/update/', updateUserProfile, name="update_profile"),
    path('profile/upload/', uploadProfileImage,name="upload_profile"),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<str:pk>/', getUserById,name="get_user"),
    path('update/<str:pk>/', updateUser,name="updateUser"),
    path('delete/<str:pk>/', deleteUser,name="deleteUser"),
    
    

]
