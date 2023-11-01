from rest_framework import generics
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.contrib.auth import authenticate, login
# API View of Events
class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Temporary homepage
def homepage(request):
    return HttpResponse("Temporary Home Page")

#Get Request that returns the notifications that a user has
def notification_view(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    notifs = Notification.objects.filter(username=name).values()
    return JsonResponse(list(notifs), safe=False, status=200)

def login(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    try:
        username = json_data.get('username')
        password = user.objects.filter(username=username).values_list('password', flat=True).first()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'error': 'Username not found'}, status=400)
    if json_data.get('password') == password:
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'Incorrect Password'}, status=400)

    # Invalid credentials, handle accordingly
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate (username = username, password = password)
        # if user is not None:
        #     login(request, user)
        #     return ('home')
        # else:
        #     return JsonResponse({'error': 'Invalid username or password.'})

# Get Request that shows all the events that a user is participating
def ViewEvents(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    name = json_data.get('username')
    events = EventUser.objects.filter(username=name).values_list('event_id', flat=True)
    participated_events = []
    for id in events:
        temp = list(Event.objects.filter(event_id = id).values())
        participants = list(EventUser.objects.filter(event_id=id).values_list('username', flat=True))
        temp[0]["participants"] = participants
        participated_events.append(temp[0])
    return JsonResponse(participated_events, safe=False, status=200)

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

# Post Request that creates a new account if username isn't already being used
class Register(CreateAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    
# Get Request that returns the events that a user is hosting
def hosted_events(request):
    try: 
        json_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Request data'}, status=400)
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
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            event_data = entire_data.get('event')
            user_data = entire_data.get('user')
            date_data = entire_data.get('date')
        except:
            return JsonResponse({"status": "Missing Input"}, status=400)

        # Precheck: checks to see if any other event has the same name before proceeding
        all_events = list(Event.objects.filter(host=event_data["host"]).values_list('name', flat=True))
        if event_data["name"] in all_events:
            return JsonResponse({'error': "That event name is currently being used by you, please try another name!"}, status=400)
        
        # Precheck: if event data is valid
        event_serializer = EventSerializer(data=event_data)
        if not event_serializer.is_valid():
            return JsonResponse({'error': "Invalid Event Info"}, status=400)
        
        # Precheck: if participant is in database
        all_users = user.objects.all().values_list('username', flat=True)
        for participant in user_data:
            if participant not in all_users:
                return JsonResponse({'error': 'User(s) Not Found!'}, status=400)

        # Precheck: if date given is in right format
        for date in date_data:
            try: 
                datetime.date.fromisoformat(date)
            except:
                return JsonResponse({'error': "Date Input Error!"}, status=400)

        # Creation of Event
        event_instance = event_serializer.save()
        
        # Adding host as sole participant in event
        host_model = {
                'event_id' : event_instance.pk,
                'username' : event_data["host"]
            }
        host_instance = EventUserSerializer(data=host_model)
        if host_instance.is_valid():
            host_instance.save()
        else:
            # Code below should theoretically never run but just in case
            event_instance.delete()
            return JsonResponse({'error': 'Host User Not Found!'}, status=400)
        
        # Sending invites to invited participants' notification box
        for participant in user_data:
            user_model = {
                'event_id' : event_instance.pk,
                'username' : participant,
                'notification' : f"You have been invited to {event_instance.name}!"
            }
            notification_serializer = NotificationSerializer(data=user_model)
            if notification_serializer.is_valid():
                notification_serializer.save()
            else:
                # Code below should theoretically never run but just in case
                event_instance.delete()
                return JsonResponse({'error': 'Could not send Invites to Invited Users'}, status=400)
            
        # Creating records for each of the event dates
        if event_data["primary_date"] not in date_data:
            date_data.append(event_data["primary_date"])
        for date in date_data:
            date_model = {
                'date' : date,
                'event_id' : event_instance.pk
            }
            date_serializer = EventDateSerializer(data=date_model)
            if date_serializer.is_valid():
                date_serializer.save()
            else:
                # Code below should theoretically never run but just in case
                event_instance.delete()
                return JsonResponse({'error': "Date Input Error!"}, status=400)
        return JsonResponse({'status': 'Success'}, status=200)

    
class Voting(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            username = entire_data.get("username")
            event_id = entire_data.get("event_id")
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)
        # Precheck: checks if notification is present
        notification_instance = Notification.objects.filter(username=username, event_id=event_id)
        if not notification_instance:
            return JsonResponse({'error':'Sorry, we cannot find this notification!'}, status=400)
        # Precheck: checks if user is in event
        event_participants = EventUser.objects.filter(event_id=event_id).values_list('username', flat=True)
        if username not in event_participants:
            notification_instance.delete()
            return JsonResponse({'error':'Sorry, either you were kicked from this event or you were never apart of it!'}, status=400)
        # Precheck: checks if event exists
        event_instance = Event.objects.get(event_id=event_id)
        if not event_instance:
            notification_instance.delete()
            return JsonResponse({'error':'Sorry, this event no longer exists!'}, status=400)
        # Adding the vote to the vote table
        vote_instance = EventVoteSerializer(data=entire_data)
        if vote_instance.is_valid():
            vote_instance.save()
        else:
            return JsonResponse({'error': str(vote_instance.errors)})
        notification_instance.delete()
        return JsonResponse({'status': 'success'}, status=200)
        
class PrimaryDate(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            event_id = entire_data["event_id"]
            date = entire_data["date"]
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)
        try:
            event = Event.objects.get(event_id = event_id)
        except:
            # Code below should theoretically never run but just in case
            return JsonResponse({'error':'No Event with this ID'}, status=400)
        
        # If primary date is the same as the proposed date, let user know
        date_check = datetime.strptime(date, "%Y-%m-%d").date()
        if date_check == event.primary_date:
            return JsonResponse({"error": "This was already the Primary Date for this Event"}, status=400)
        
        event.primary_date = date
        event.save()
        return JsonResponse({"status": 'success'}, status=200)
    
class LeaveEvent(CreateAPIView):
    def create(self, request, *args, **kwargs):
        #needs to remove from EventUser, Vote, Availability
        # Extracting data from request and checking missing information
        try: 
            entire_data = request.data
            event_id = entire_data['event_id']
            username = entire_data['username']
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)

        # PreCheck: check if the participant is the host
        event = Event.objects.filter(event_id=event_id).first()
        if username == str(event.host):
            return JsonResponse({'error':'The Host cannot leave the Event, Try deleting the Event instead!'}, status=400)
        
        # Precheck: see if the user is actually in that event before removing
        participants = EventUser.objects.filter(event_id=event_id).values_list('username', flat=True)
        if username not in participants:
            return JsonResponse({'error':'Participant already not in Event'}, status=400)
        
        # Remove from EventUser
        delete_eventuser = EventUser.objects.filter(event_id=event_id, username=username).first()
        delete_eventuser.delete()
        
        # Remove from Vote
        user_votes = Vote.objects.filter(event_id=event_id, username=username)
        user_votes.delete()
        
        # Remove from Availability
        user_availabilities = Availability.objects.filter(event_id=event_id, username=username)
        user_availabilities.delete()
        return JsonResponse({"status":"success"}, status=200)
    
class Reject(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        try:
            entire_data = request.data
            username = entire_data.get("username")
            event_id = entire_data.get("event_id")
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)
        notification_instance = Notification.objects.filter(event_id=event_id, username=username)
        if not notification_instance:
            return JsonResponse({'error': "No notification found for this event/participant."}, status=400)
        notification_instance.delete()
        return JsonResponse({"status":"success"}, status=200)

class Delete(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            entire_data = request.data
            username = entire_data.get("username")
            event_id = entire_data.get("event_id")
        except:
            return JsonResponse({'error':'Missing Input'}, status=400)
        delete_event = Event.objects.filter(event_id=event_id).first()
        if not delete_event:
            return JsonResponse({'error': "Event not found"}, status=400)
        if str(delete_event.host) != username:
            return JsonResponse({'error': "You don't have the authority to delete this event!"}, status=400)
        delete_event.delete()
        return JsonResponse({"status":"success"}, status=200)
        
        
