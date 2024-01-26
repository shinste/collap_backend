from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Event, user
from ..serializers import EventSerializer, EventUserSerializer, NotificationSerializer, EventDateSerializer, EventAvailabilitySerializer
from datetime import datetime

# Post Request that creates an event, invites participants, adds available dates
class CreateEvent(CreateAPIView):
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Extracting data from request and checking missing information
            entire_data = request.data
            event_data = entire_data.get('event')
            user_data = entire_data.get('user')
            date_data = entire_data.get('date')
            
            if not event_data or not user_data or not date_data:
                return JsonResponse({"error": "Missing Input"}, status=400)

            # Precheck: checks to see if any other event has the same name before proceeding
            all_events = list(Event.objects.filter(host=event_data["host"]).values_list('name', flat=True))
            if event_data["name"] in all_events:
                return JsonResponse({'error': "That event name is currently being used by you, please try another name!"}, status=400)
            
            # Precheck: if event data is valid
            event_serializer = EventSerializer(data=event_data)
            if not event_serializer.is_valid():
                return JsonResponse({'error': event_serializer.errors}, status=400)
            
            # Precheck: if participant is in database
            all_users = user.objects.all().values_list('username', flat=True)
            for participant in user_data:
                if participant not in all_users:
                    return JsonResponse({'error': 'User(s) Not Found!'}, status=400)

            # Precheck: if date given is in right format
            for curr_date in date_data:
                try: 
                    datetime.fromisoformat(curr_date)
                except:
                    return JsonResponse({'error': "Date Input Error!"}, status=400)

            # Creation of Event
            event_instance = event_serializer.save()
            
            try:
                # Adding host as sole participant in event
                host_model = {
                        'event_id' : event_instance.pk,
                        'username' : event_data["host"]
                    }
                host_instance = EventUserSerializer(data=host_model)
            except Exception as e:
                return JsonResponse({'error': str(e)})
                
                
            if host_instance.is_valid():
                host_instance.save()
            else:
                # Code below should theoretically never run but just in case
                event_instance.delete()
                return JsonResponse({'error': str(host_instance.errors)}, status=400)
            
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
            # Availability Insert
            for date in date_data:
                availability = {
                    'date': date,
                    'event_id' : event_instance.pk,
                    'username' : user_data
                }
                availability_instance = EventAvailabilitySerializer(data=availability)
                if availability_instance.is_valid():
                    availability_instance.save()
                
            
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)})