from rest_framework.generics import CreateAPIView
from django.http import HttpResponse
class Homepage(CreateAPIView):
    def create(self, request, *args, **kwargs):
        return HttpResponse("Temporary Home Page")