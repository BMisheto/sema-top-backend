# Django Import
from cgitb import lookup
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status
# Rest Framework Import
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView, ListAPIView,ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from events.serializers import EventSerializer,AttendeeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from  events.models import *


# Get all events
@api_view(['GET'])
def getEvents(request):
    query = request.query_params.get("keyword")
    if query == None:
        query = ''
    lookup = Q(name__icontains=query)  
    events = Event.objects.filter(lookup).order_by('-_id')
    events_count = Event.objects.all().count()
    

    serializer = EventSerializer(events , many=True)
    return Response({'events': serializer.data,'count':events_count })


# Get all My events
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyEvents(request,pk):
    query = request.query_params.get("keyword")
    user = User.objects.get(id=pk)
    if query == None:
        query = ''
    lookup = Q(name__icontains=query)  
    events = Event.objects.filter(user=user).filter(lookup).order_by('-_id')
    events_count = Event.objects.filter(user=user).filter(lookup).count()
    

    serializer = EventSerializer(events , many=True)
    return Response({'events': serializer.data,'count':events_count})





# Get event
@api_view(['GET'])
def getEvent(request, pk):
    event = Event.objects.get(_id=pk)
    serializer = EventSerializer(event , many=False)
    return Response({"event":serializer.data})


# Get Attendance
@api_view(['GET'])
def getAttendance(request,pk):
    event = Event.objects.get(_id=pk)
    attending = Attendee.objects.filter(event=event).order_by('-_id')
    attending_count = Attendee.objects.filter(event=event).count()
    serializer =AttendeeSerializer(attending , many=True)
    return Response({'attending': serializer.data,'count':attending_count })


# add event
@api_view(['POST'])
@permission_classes([IsAdminUser])
def createEvent(request):
    user = request.user
    event = Event.objects.create(
        user=user,
        name="New Event Name ",
        venue=" Venue ",
        location="Location",
        start_date="Start Date",
        end_date="End Date",
        description="Description",
    )

    serializer = EventSerializer(event, many=False)
    return Response(serializer.data)

# # create new event
# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def createNewEvent(request):
#     user = request.user
#     data = request.data
#     event = Event.objects.create(
#         user=user,
#         name=data['name'],
#         venue=data['venue'],
#         location=data['location'],
#         start_date=data['start_date'],
#         end_date=data['end_date'],
#         description=data['description'],
#     )

#     serializer = EventSerializer(event, many=False)
#     return Response(serializer.data)


# Create New Donations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createNewEvent(request):
    user = request.user
    data = request.data
    



    # get the uploaded image from request data
    image = request.FILES.get('event_cover')

    event = Event.objects.create(
        user=user,
        name=data['name'],
        venue=data['venue'],
        location=data['location'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        description=data['description'],
        event_cover=image  # save the image to the donation model
    )

    serializer = EventSerializer(event , many=False)
    return Response({"event":serializer.data})


# update event
# Update single products
@api_view(['PUT'])
@permission_classes([IsAdminUser, IsAuthenticated])
def updateEvent(request, pk):
    data = request.data
    event = Event.objects.get(_id=pk)
    event.name = data["name"]
    event.description = data["description"]
    event.start_date = data["start_date"]
    event.end_date = data["end_date"]
    event.venue = data["venue"]
    event.location = data["location"]
    event.event_cover = request.FILES.get('event_cover')
   

    event.save()

    serializer = EventSerializer(event, many=False)
    return Response({"event":serializer.data})



# upload event image
@api_view(['POST'])
def uploadEventCover(request):
    data = request.data
    event_id = data['event_id']
    event = Event.objects.get(_id=event_id)
    event.event_cover = request.FILES.get('image')
    event.save()
    return Response("Image was uploaded")

# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteEvent(request, pk):
    event = Event.objects.get(_id=pk)
    event.delete()
    return Response("Poll deleted successfully")




@api_view(['POST'])
def addAttendee(request, pk):
    data = request.data
    user_id = data['user']
    event = Event.objects.get(_id=pk)
    user = User.objects.get(id=user_id)

    # Check if the user is already an attendee of the event
    if Attendee.objects.filter(user=user_id).exists():
        return Response('User already in the list')

    attendee = Attendee.objects.create(
        user=user,
        event=event,
    )

    serializer = AttendeeSerializer(attendee, many=False)
    return Response('User added to list')



@api_view(['DELETE'])
def removeAttendee(request, pk):
    data = request.data
    event = Event.objects.get(_id=pk)
    user_id = data['event']['user']
    user = User.objects.get(id=user_id)
    try:
        attendee = Attendee.objects.filter(event=event).get(user=user)
        attendee.delete()
        return Response('Attendee removed')
    except Attendee.DoesNotExist:
        return Response('Attendee not found')


