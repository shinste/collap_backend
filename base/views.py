from rest_framework import generics
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, login

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

# def Login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate (username = username, password = password)
#         if user is not None:
#             login(request, user)
#             return ('home')
#         else:
#             return JsonResponse({'error': 'Invalid username or password.'})
#     else:

def ViewEvents(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    events = UserEvent.objects.filter(username=name).values()
    return JsonResponse(list(events), safe=False, status=200)

def GetVotes(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    event_id = json_data.get('event_id')
    if event_id is None:
        return JsonResponse({'error': 'event_id is missing'}, status=400)

    votes = Vote.objects.filter(event_id=event_id).values()
    return JsonResponse(list(votes), safe=False, status=200)
