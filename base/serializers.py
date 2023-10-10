from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = 'all'

class EventUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'all'

class EventVote(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = 'all'

class EventUserEvent(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = 'all'

class EventNotifications(serializers.ModelSerializer):
    class Meta:
        model = EventNotifications
        fields = 'all'

class EventAvailability(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = 'all'

class EventEventData(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = 'all'