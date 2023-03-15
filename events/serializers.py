from rest_framework import serializers
from rest_framework.reverse import reverse
from events.models import Event,Attendee





class EventSerializer(serializers.ModelSerializer):
    attendees = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Event
        fields= '__all__'
    def get_attendees(self,obj):
        attendees = obj.attendee_set.all().count()
        return attendees


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendee
        fields= '__all__'