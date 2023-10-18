from django.urls import path
from .views import *
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.Homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path('event/view/', EventView.as_view(), name="event"),
    path('notification/', views.NotificationView , name="notifications"),
    path('user/view_events/', views.ViewEvents, name='view_events'),
    path('event/get_votes/', views.GetVotes, name="get_votes")
]
