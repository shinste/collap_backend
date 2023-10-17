from rest_framework import generics
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import json

class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

def Homepage(request):
    return HttpResponse("Temporary Home Page")

def NotificationView(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    notifs = Notification.objects.filter(username=name).values()
    return JsonResponse(list(notifs), safe=False, status=200)

#Post Request that creates a new account if username isn't already being used
class Register(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    
#Get Request that returns the events that a user is hosting
def HostedEvents(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    hosted_events = Event.objects.filter(host=name).values()
    return JsonResponse(list(hosted_events), safe=False, status=200)

#Utility Function that ranks the possible dates by people available and displays who aren't for each
def RankDates(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    #grab all availability associated with the event
    id = json_data.get('event_id')
    availability = Availability.objects.filter(event_id_id=id).values()
    
    #dictionary with key as date and value as participants who aren't available for that date
    ranked = {}
    #list of participants in the event
    participants = list(Availability.objects.filter(event_id_id=id).values_list('username_id', flat=True).distinct())
    #goes through each availability and removes user if they are available for that date
    for entry in availability:
        date = str(entry['date'])
        if date not in ranked.keys():
            ranked[date] = participants.copy()
        ranked[date].remove(entry['username_id'])
    #sorts dictionary keys (dates) from least amount of unavailable participants to most
    sorted_dates = sorted(ranked, key=lambda k: len(ranked[k]), reverse=False)
    return JsonResponse({key: ranked[key] for key in sorted_dates}, safe=False, status=200)
    
        
    
    # 


    
