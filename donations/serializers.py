
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.db.models import Sum
from .models import *
from donations.models import *



# PDonation serializers
class DonationSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Donation
        fields = "__all__"
    def get_total(self,obj):
        total_amount = obj.transaction_set.aggregate(Sum('amount'))['amount__sum']
        return total_amount


# Donator Serializers
class DonatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donator
        fields = "__all__"


