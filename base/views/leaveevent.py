from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Availability, EventUser, Event, Vote, Notification
from base.serializers import NotificationSerializer

#Post Request that removes a person from an event
class LeaveEvent(CreateAPIView):
    def create(self, request, *args, **kwargs):
        #needs to remove from EventUser, Vote, Availability
        # Extracting data from request and checking missing information
        entire_data = request.data
        event_id = entire_data.get('event_id')
        username = entire_data.get('username')
        try:
            if not event_id or not username:
                return JsonResponse({"error":"Missing Input"},status=400)

            
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
            
            # Remove from Notification and notify user of removal
            event_notifications = Notification.objects.filter(event_id=event_id, username=username)
            event_notifications.delete()
            notification_instance = NotificationSerializer(data = {'event_id': event_id,
                                                                'username': username,
                                                                'notification': f"You are no longer in the event: {event.name}!"})
            if notification_instance.is_valid():
                notification_instance.save()
            else:
                return JsonResponse({'error': str(notification_instance.errors)}, status=400)
            
            # Remove from Availability
            user_availabilities = Availability.objects.filter(event_id=event_id, username=username)
            user_availabilities.delete()

            try:
                participants = EventUser.objects.filter(event_id=event_id).values_list('username', flat=True)
                for name in participants:
                    if name != username:

                        notif_data = {
                            'event_id': event_id,
                            'username': name,
                            'notification': f"{username} is no longer in {event.name}!"
                        }
                        if not Notification.objects.filter(event_id=event_id, username=name, notification=f"{username} is no longer in {event.name}!").exists():
                            joining_notif = NotificationSerializer(data=notif_data)
                            if joining_notif.is_valid():
                                joining_notif.save()
            except Exception as e:

                return JsonResponse({'error': f'{e}'}, status=400)

            return JsonResponse({"status":"success"}, status=200)
        except Exception as e:
                return JsonResponse({'error': f'{e}'}, status=400)