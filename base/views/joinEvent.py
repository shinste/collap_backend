from rest_framework.generics import CreateAPIView
from ..models import *
from ..serializers import *
from django.http import JsonResponse
import re

class JoinEvent(CreateAPIView):
    def validate_date_format(self, date):
        # Validate that the date has the format YYYY-MM-DD.
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        return bool(date_pattern.match(date))

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
            return JsonResponse({'error': 'Event not found'}, status=400)

        # Validate date format
        for date in date_data:
            if not self.validate_date_format(date):
                return JsonResponse({'error': f'Invalid date format, {date}'}, status=400)

        # Check if date list is empty
        if not date_data:
            return JsonResponse({'error': 'No dates provided'}, status=400)

        user_event_data = {
            'username': user_data,
            'event_id': event_id_data
        }

        # Create the UserEvent object
        user_event_serializer = EventUserSerializer(data=user_event_data)
        if user_event_serializer.is_valid():
            user_event_serializer.save()
        else:
            return JsonResponse(user_event_serializer.errors, status=400)

        for date in date_data:
            if EventDate.objects.filter(event_id=event_id_data, date=date).exists():
                # If the EventDate already exists, continue on to add availbility operation
                pass
            else:
                current_date_data = {
                    'event_id': event_id_data,
                    'date': date
                }
                event_date_serializer = EventDateSerializer(data=current_date_data)
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
