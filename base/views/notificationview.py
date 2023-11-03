from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import Notification

class NotificationView(ListAPIView):
    def list(self, request, *args, **kwargs):
        # try:
        #     json_data = json.loads(request.body.decode('utf-8'))
        # except json.JSONDecodeError:
        #     return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        # username = json_data.get("username")
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        notifs = Notification.objects.filter(username=username).values()
        #return JsonResponse(username, safe=False, status=200)
        return JsonResponse(list(notifs), safe=False, status=200)