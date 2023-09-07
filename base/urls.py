from django.urls import path
from . import views
from .views import EventView

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', EventView.as_view())
]
