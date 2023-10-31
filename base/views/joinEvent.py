from rest_framework.generics import CreateAPIView
from ..models import *
from ..serializers import *
from django.http import JsonResponse
import json

class joinEvent(CreateAPIView):

    def create(self, request, *args, **kwargs):
        # Extract data from the request
        data = request.data
        user_data = data.get('username')
        event_id_data = data.get('event_id')
        date_data = data.get('dates')

        try:
            # Attempt to retrieve the event object using the provided event_id
            event = Event.objects.get(event_id=event_id_data)
            event_name = event.name
        except Event.DoesNotExist:
            # If the event does not exist, return an error response
            return JsonResponse({'error': 'Event not found'}, status=404)

        user_event_data = {
            'username': user_data,
            'event_id': event_id_data
        }

        # Create the UserEvent object
        user_event_serializer = EventUserSerializer(data=user_event_data)
        if user_event_serializer.is_valid():
            user_event_serializer.save()
        else:
            # If there are errors in the serializer, return a response with the errors
            return JsonResponse(user_event_serializer.errors, status=400)

        for date in date_data:
            if EventDate.objects.filter(event_id=event_id_data, date=date).exists():
                # If the EventDate already exists, continue to the next date
                pass
            else:
                temp_date_data = {
                    'event_id': event_id_data,
                    'date': date
                }
                event_date_serializer = EventDateSerializer(data=temp_date_data)
                if event_date_serializer.is_valid():
                    event_date_serializer.save()
                else:
                    # If there are errors in the serializer, return a response with the errors
                    return JsonResponse(event_date_serializer.errors, status=400)

            if Availability.objects.filter(event_id=event_id_data, username=user_data, date=date).exists():
                # If the Availability entry already exists, continue to the next date
                continue

            availability_data = {
                'event_id': event_id_data,
                'username': user_data,
                'date': date
            }

            # Create an Availability entry
            availability_date_serializer = EventAvailabilitySerializer(data=availability_data)
            if availability_date_serializer.is_valid():
                availability_date_serializer.save()
            else:
                # If there are errors in the serializer, return a response with the errors
                return JsonResponse(availability_date_serializer.errors, status=400)

        if Notification.objects.filter(event_id=event_id_data, username=user_data).exists():
            # If a notification for this event and user already exists, delete it
            notification_to_delete = Notification.objects.get(event_id=event_id_data, username=user_data)
            notification_to_delete.delete()

        # Return a success response
        return JsonResponse({'status': 'success'}, status=200)
