from rest_framework.generics import CreateAPIView
from ..models import *
from ..serializers import *
from django.http import JsonResponse
import re
import datetime

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
        date_data = data.get('date')

        if not user_data or not event_id_data or not date_data:
            return JsonResponse({'error':'Missing Input'}, status=400)
        try:
            # Attempt to retrieve the event object using the provided event_id
            event = Event.objects.get(event_id=event_id_data)
        except :
            return JsonResponse({'error': 'Event Not Found'}, status=400)

        # Validate date format
        for date in date_data:
            if not self.validate_date_format(date):
                return JsonResponse({'error': f'Invalid date format, {date}'}, status=400)

        # Check if date list is empty
        if not date_data:
            return JsonResponse({'error': 'No dates provided'}, status=400)
        
        # Checks if use is already in event, deletes notification if already in
        if EventUser.objects.filter(event_id=event_id_data, username=user_data).exists():
            return JsonResponse({'error': 'User already in event'}, status=400)
        

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

        try:
            for date in date_data:
                if not EventDate.objects.filter(event_id=event_id_data, date=date).exists():
                    # If the EventDate already exists, continue on to add availbility operation
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
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status=400)
            

        if Notification.objects.filter(event_id=event_id_data, username=user_data).exists():
            # If a notification for this event and user already exists, delete it
            notification_to_delete = Notification.objects.filter(event_id=event_id_data, username=user_data)
            notification_to_delete.delete()

        try:
            participants = EventUser.objects.filter(event_id=event_id_data).values_list('username', flat=True)
            for name in participants:
                if name != user_data:
                    notif_data = {
                        'event_id': event_id_data,
                        'username': name,
                        'notification': f"{user_data} has joined {event.name}!"
                    }
                    if not Notification.objects.filter(event_id=event_id_data, username=name, notification=f"{user_data} has joined {event.name}!").exists():
                        joining_notif = NotificationSerializer(data=notif_data)
                        if joining_notif.is_valid():
                            joining_notif.save()
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status=400)
        # Return a success response
        return JsonResponse({'status': 'success'}, status=200)