# going from a python object to json
from rest_framework import serializers
from .models import *



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','date', 'name', 'date_created', 'participants')