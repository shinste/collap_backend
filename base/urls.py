from django.urls import path
from .views import *
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.Homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path('event/view/', EventView.as_view(), name="event"),
    path('notification/', views.NotificationView , name="notifications"),
    path('register/', Register.as_view(), name="register"),
    path('hosted/', views.HostedEvents, name="hosted events"),
    path('ranked/', views.RankDates, name="rank")
    # path('event/create/', CreateEvent.as_view(), name="event")
]
