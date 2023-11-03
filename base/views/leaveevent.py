from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Availability, EventUser, Event, Vote


#Post Request that removes a person from an event
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