from django.urls import path
from donations.views import *


urlpatterns = [

     # add an event
    path('create/', createNewDonation,name="create-new-donation"),
    # add an event
    path('add/', createDonation,name="add-donation"),
    # get all events
    path('', getDonations,name="donations"),


    path('<str:pk>/mydonations/', getMyDonations,name="my-donations"),

    # get event
    path('<str:pk>/', getDonation,name="get-donation"),
    

    # add an event
    path('add/', createDonation,name="add-donation"),


    path('delete/<str:pk>/', deleteDonation,name="delete-donation"),


   

    # update event
    path('update/<str:pk>/', updateDonation,name="update-donation"),

    # upload event
    path('upload/cover/', uploadDonationCover,name="upload-cover"),


    
    
]
