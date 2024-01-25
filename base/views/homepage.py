from rest_framework.generics import CreateAPIView
from django.http import HttpResponse
class Homepage(CreateAPIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Home Page")