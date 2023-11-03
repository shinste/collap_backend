from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from ..models import user

class Login(ListAPIView):
    def list(self, request, *args, **kwargs):
        username = request.GET.get('username')
        password = request.GET.get('password')
        if username is None:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        try:
            databasepassword = user.objects.filter(username=username).values_list('password', flat=True).first()
        except:
            return JsonResponse({'error': 'Username not found'}, status=400)
        if databasepassword == password:
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'error': 'Incorrect Password'}, status=400)