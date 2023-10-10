# going from a python object to json
from rest_framework import serializers
from .models import *



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EventVote(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class EventUserEvent(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = '__all__'

class EventNotifications(serializers.ModelSerializer):
    class Meta:
        model = EventNotifications
        fields = '__all__'

class EventAvailability(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class EventEventData(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = '__all__'


