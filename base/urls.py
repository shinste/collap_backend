from django.urls import path
from .views import *
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path('event/view/', EventView.as_view(), name="event view"),
    path('notification/', views.notification_view , name="notifications"),
    path('register/', Register.as_view(), name="register"),
    path('hosted/', views.hosted_events, name="hosted events"),
    path('ranked/', views.rank_dates, name="rank"),
    path('event/create/', CreateEvent.as_view(), name="create event"),
    path('event/view/', EventView.as_view(), name="event"),
    path('notification/', views.NotificationView , name="notifications"),
    path('user/view_events/', views.ViewEvents, name='view_events'),
    path('event/get_votes/', views.GetVotes, name="get_votes")
]
