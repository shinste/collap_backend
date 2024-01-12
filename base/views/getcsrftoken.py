from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

@method_decorator(ensure_csrf_cookie, name='dispatch')
class getcsrf(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        return JsonResponse({'Success': 'CSRF Cookie set'})