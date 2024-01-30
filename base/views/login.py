from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from ..models import user

# Get Request that checks the username's password in database (temporary?)
class Login(CreateAPIView):
    def create(self, request, *args, **kwargs):
        entire_data = request.data
        username = entire_data.get('username')
        password = entire_data.get('password')

        if not username or not password:
            return JsonResponse({'error':'Missing Input'}, status=400)
        try:
            databasepassword = user.objects.filter(username=username).values_list('password', flat=True).first()
        except:
            return JsonResponse({'error': 'Username not found'}, status=400)
        if databasepassword == password:
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'error': 'Incorrect Password'}, status=400)