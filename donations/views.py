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




# Local Import
from donations.serializers import *
from donations.models import *





# Create your views here.

# Get Donations
@api_view(['GET'])
def getDonations(request):
    query = request.query_params.get("keyword")
    if query == None:
        query = ''
    lookup = Q(name__icontains=query)  
    donations = Donation.objects.filter(lookup).order_by('-_id')
    donations_count = Donation.objects.filter(lookup).count()
    
    

    serializer = DonationSerializer(donations , many=True)
    return Response({"donations": serializer.data, "count":donations_count})


# Get MY Donations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyDonations(request,pk):
    query = request.query_params.get("keyword")
    user = User.objects.get(id=pk)
    if query == None:
        query = ''
    lookup = Q(name__icontains=query)  
    donations = Donation.objects.filter(user=user).filter(lookup).order_by('-_id')
    donations_count = Donation.objects.filter(user=user).filter(lookup).count()
    
    

    serializer = DonationSerializer(donations , many=True)
    return Response({"donations": serializer.data, "count":donations_count})


# Get Donations
@api_view(['GET'])
def getDonation(request,pk):
    donation = Donation.objects.get(_id=pk)
    serializer = DonationSerializer(donation , many=False)
    return Response({"donation":serializer.data})


# Create Donations
@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def createDonation(request):
    user = request.user
    donation = Donation.objects.create(
        user=user,
        name="Donation Name",
        description="Donation Description",
        target=0,
    )
   

    serializer = DonationSerializer(donation , many=False)
    return Response({"donation":serializer.data})



# # Create New Donations
# @api_view(['POST'])
# @permission_classes([IsAdminUser, IsAuthenticated])
# def createNewDonation(request):
#     user = request.user
#     data = request.data
#     print(data)
#     donation = Donation.objects.create(
#         user=user,
#         name=data['name'],
#         description=data['description'],
#         target=data['target'],
#     )
   
   

#     serializer = DonationSerializer(donation , many=False)
#     return Response({"donation":serializer.data})

# Create New Donations
@api_view(['POST'])
@permission_classes([ IsAuthenticated])
def createNewDonation(request):
    user = request.user
    data = request.data

    # get the uploaded image from request data
    image = request.FILES.get('donation_cover')

    donation = Donation.objects.create(
        user=user,
        name=data['name'],
        description=data['description'],
        target=data['target'],
        donation_cover=image  # save the image to the donation model
    )

    serializer = DonationSerializer(donation , many=False)
    return Response({"donation":serializer.data})



# Update Donations
@api_view(['PUT'])
@permission_classes([IsAdminUser, IsAuthenticated])
def updateDonation(request,pk):
    data = request.data
    donation = Donation.objects.get(_id=pk)
    donation.name = data["name"]
    donation.description = data["description"]
    donation.target = data["target"]
    donation.donation_cover = request.FILES.get('donation_cover')

    donation.save()

    serializer = DonationSerializer(donation , many=False)
    return Response({"donation":serializer.data})



# Upload Donation Cover
@api_view(['POST'])
def uploadDonationCover(request):
    data = request.data
    donation_id = data['donation_id']
    donation = Donation.objects.get(_id=donation_id)
    donation.donation_cover = request.FILES.get('image')
    donation.save()
    return Response("Image was uploaded")


# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteDonation(request, pk):
    donation = Donation.objects.get(_id=pk)
    donation.delete()
    return Response("Poll deleted successfully")


