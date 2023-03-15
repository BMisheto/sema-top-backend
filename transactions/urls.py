from django.urls import path
from transactions.views import *


urlpatterns = [
    # get all transactions
    path('', getTransactions,name="transactions"),

    
    # get tranaction
    path('<str:pk>/', getTransaction,name="get-transaction"),
    

    # add a transaction
    path('add/', createTransaction,name="add-transaction"),

  


    
    
]
