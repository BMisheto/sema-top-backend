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
from events.serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from  transactions.models import *
from  transactions.serializers import *



# Get all transactions
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getTransactions(request): 
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


# Get all transactions
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getTransaction(request,pk): 
    transactions = Transaction.objects.get(_id=pk)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)




# Get all transactions
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getTransaction(request,pk): 
    transactions = Transaction.objects.get(_id=pk)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)



# create transaction
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def createTransaction(request):
    user = request.user
    donation = request.donation
    transaction = Transaction.objects.create(
        user=user,
        donation=donation,
        amount=0,
        
    )

    serializer = TransactionSerializer(transaction, many=False)
    return Response(serializer.data)


