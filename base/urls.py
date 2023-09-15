from django.urls import path
from . import views
from .views import EventView

urlpatterns = [
    path('', EventView.as_view(), name="event"),
]
