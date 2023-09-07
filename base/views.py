from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .serializers import EventSerializer
from rest_framework import generics

# Create your views here.

class EventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

def home(request):
    return HttpResponse('Home Page')

