from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Notification, Event, EventUser, EventDate
from ..serializers import NotificationSerializer, EventDateSerializer

#Post Request invites users
class EditDate(CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Extracting data from request and checking missing information
        entire_data = request.data
        dates = entire_data.get("date")
        event_id = entire_data.get("event_id")
        action = entire_data.get("action")
        if not dates or not event_id or not action:
            return JsonResponse({'error':'Missing Input'}, status=400)

        if action == 'delete':
            try:
                for date in dates:
                    event_date = EventDate.objects.get(event_id=event_id, date=date)
                    if event_date:
                        event_date.delete()
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            all_dates = EventDate.objects.filter(event_id=event_id).values_list('date', flat=True)
            if dates in all_dates:
                return JsonResponse({'error': 'Date already added to Event'}, status=400)
            else:
                new_date = {
                    'event_id': event_id,
                    'date' : dates
                }
                event_date_instance = EventDateSerializer(data=new_date)
                if event_date_instance.is_valid():
                    event_date_instance.save()
                else:
                    return JsonResponse({event_date_instance.errors}, status=400)
        return JsonResponse({"status":"success"}, status=200)
