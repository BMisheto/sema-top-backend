from django.urls import path
from events.views import *


urlpatterns = [

 
    # create an event
    path('create/', createNewEvent,name="create-new-event"),

     # add attendee
    path('attending/add/<str:pk>/', addAttendee,name="add-attendee"),

     # remove from attendance
    path('attending/remove/<str:pk>/', removeAttendee,name="remove-attendance"),

    # add an event
    path('add/', createEvent,name="add-event"),

   
    # get all events
    path('', getEvents,name="events"),

    # get my events
    path('<str:pk>/myevents/', getMyEvents,name="my-events"),


    # get event
    path('<str:pk>/', getEvent,name="get-event"),

       # list attendance
    path('attendance/<str:pk>/', getAttendance,name="get-attendance"),


     # add an event
    path('add/', createEvent,name="add-event"),


     # update event
    path('update/<str:pk>/', updateEvent,name="update-event"),

    # upload event
    path('upload/cover/', uploadEventCover,name="upload-cover"),

    # delete event
    path('delete/<str:pk>/', deleteEvent,name="delete-event"),



   


    
    
]
