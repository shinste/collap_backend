from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import Event

# Post Request that deletes an event entirely
class Delete(CreateAPIView):
    def create(self, request, *args, **kwargs):
        
        entire_data = request.data
        username = entire_data.get("username")
        event_id = entire_data.get("event_id")
        if not event_id or not username:
            return JsonResponse({'error':'Missing Input'}, status=400)
        delete_event = Event.objects.filter(event_id=event_id).first()
        if not delete_event:
            return JsonResponse({'error': "Event not found"}, status=400)
        if str(delete_event.host) != username:
            return JsonResponse({'error': "You don't have the authority to delete this event!"}, status=400)
        delete_event.delete()
        return JsonResponse({"status":"success"}, status=200)