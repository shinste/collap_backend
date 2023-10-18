from rest_framework import generics
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import json

# API View of Events
class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Temporary homepage
def homepage(request):
    return HttpResponse("Temporary Home Page")

# Get Request that returns the notifications that a user has
def notification_view(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    notifs = Notification.objects.filter(username=name).values()
    return JsonResponse(list(notifs), safe=False, status=200)

# Post Request that creates a new account if username isn't already being used
class Register(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    
# Get Request that returns the events that a user is hosting
def hosted_events(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    hosted_events = Event.objects.filter(host=name).values()
    return JsonResponse(list(hosted_events), safe=False, status=200)

# Get Request that returns a ranked list of possible dates and who is unable to make
# each date
def rank_dates(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    event_id = json_data.get('event_id')
    availability = Availability.objects.filter(event_id_id=event_id).values()
    ranked = {}
    participants = list(Availability.objects.filter(event_id_id=event_id).values_list('username_id', flat=True).distinct())
    # goes through each availability and removes user if they are available for that date
    for entry in availability:
        date = str(entry['date'])
        if date not in ranked.keys():
            ranked[date] = participants.copy()
        ranked[date].remove(entry['username_id'])
    # sorts dictionary keys (dates) from least amount of unavailable participants to most
    sorted_dates = sorted(ranked, key=lambda k: len(ranked[k]), reverse=False)
    return JsonResponse({key: ranked[key] for key in sorted_dates}, safe=False, status=200)
    
        

# POST Request that handles everything to do with creating an Event
class CreateEvent(CreateAPIView):
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        entire_data = request.data
        event_data = entire_data.get('event')
        user_data = entire_data.get('user')
        date_data = entire_data.get('date')
        
        # checks to see if any other event has the same name before proceeding
        all_events = list(Event.objects.filter(host=event_data["host"]).values_list('name', flat=True))
        if event_data["name"] in all_events:
            return JsonResponse({'error': "That event name is currently being used by you, please try another name!"}, status=400)
        
        # creating event record
        event_serializer = EventSerializer(data=event_data)
        if event_serializer.is_valid():
            event_instance = event_serializer.save()
        else:
            return JsonResponse({'error': "Invalid Event Info"}, status=400)
        
        # creating records for each of the event users
        try:
            if event_data["host"] not in user_data:
                user_data.append(event_data["host"])
            for participant in user_data:
                user_model = {
                    'event_id' : event_instance.pk,
                    'username' : participant
                }
                user_serializer = EventUserSerializer(data=user_model)
                if not user_serializer.is_valid():
                    event_instance.delete()
                    return JsonResponse({'error': 'User(s) Not Found!'}, status=400)
                user_instance = user_serializer.save()
        except Exception as e:
            event_instance.delete()
            return JsonResponse({'error': str(e)}, status=400)
        try:
            # adding an invite notification to specified users notification inbox
            user_model["notification"] = f"You have been invited to {event_instance.name}!"
            notification_serializer = NotificationSerializer(data=user_model)
            if notification_serializer.is_valid():
                notification_instance = notification_serializer.save()
            else:
                event_instance.delete()
                user_instance.delete()
                return JsonResponse({'error': 'User(s) Not Found!'}, status=400)
        except Exception as e:
            # talk to brandon about deleting
            event_instance.delete()
            user_instance.delete()
            return JsonResponse({'error': str(e)}, status=400)

        # creating records for each of the event dates
        try: 
            if event_data["primary_date"] not in date_data:
                date_data.append(event_data["primary_date"])
            for date in date_data:
                date_model = {
                    'date' : date,
                    'event_id' : event_instance.pk
                }
                date_serializer = EventDateSerializer(data=date_model)
                if not date_serializer.is_valid():
                    user_instance.delete()
                    event_instance.delete()
                    notification_instance.delete()
                    return JsonResponse({'error': "Date Input Error!"}, status=400)
                date_serializer.save()
        except Exception as e:
            # talk to brandon about deleting
            user_instance.delete()
            event_instance.delete()
            notification_instance.delete()
            return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({'status': 'Success'}, status=200)

            
        
    
