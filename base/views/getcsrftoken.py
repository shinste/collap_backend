from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token

@method_decorator(ensure_csrf_cookie, name='dispatch')
class get_csrf_view(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        get_token()
        return JsonResponse({'Success': 'CSRF Cookie set'})