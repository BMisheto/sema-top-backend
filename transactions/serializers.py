from rest_framework import serializers
from rest_framework.reverse import reverse
from transactions.models import *




# Transctions serializers
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields= '__all__'
