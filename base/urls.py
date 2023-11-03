from django.urls import path
from .views import *
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path('event/view/', views.ViewEvents, name="event view"),
    path('notification/', views.notification_view , name="notifications"),
    path('register/', Register.as_view(), name="register"),
    path('hosted/', views.hosted_events, name="hosted events"),
    path('ranked/', views.rank_dates, name="rank"),
    path('event/create/', CreateEvent.as_view(), name="create event"),
    path('notification/', views.notification_view, name="notifications"),
    path('user/view_events/', views.ViewEvents, name='view_events'),
    path('event/get_votes/', views.GetVotes, name="get_votes"),
    path('vote/', Voting.as_view(), name="vote"),
    path('primary/', PrimaryDate.as_view(), name="set primary"),
    path('event/leave/', LeaveEvent.as_view(), name="leave"),
    path('login/', views.login, name='login'),
    path('reject/', Reject.as_view(), name='reject'),
    path('event/delete/', Delete.as_view(), name='delete')
]
