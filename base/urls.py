from django.urls import path
from .views.createevent import CreateEvent
from .views.delete import Delete
from .views.homepage import Homepage
from .views.hostedevents import HostedEvents
from .views.leaveevent import LeaveEvent
from .views.login import Login
from .views.notificationview import NotificationView
from .views.primarydate import PrimaryDate
from .views.rankdates import RankDates
from .views.register import Register
from .views.deletenotification import DeleteNotifications
from .views.viewevents import ViewEvents
from .views.voting import Voting
from django.contrib import admin

urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('admin/', admin.site.urls),
    path('event/view/', ViewEvents.as_view(), name="event view"),
    path('notification/', NotificationView.as_view() , name="notifications"),
    path('register/', Register.as_view(), name="register"),
    path('hosted/', HostedEvents.as_view(), name="hosted events"),
    path('ranked/', RankDates.as_view(), name="rank"),
    path('event/create/', CreateEvent.as_view(), name="create event"),
    path('notification/', NotificationView.as_view(), name="notifications"),
    path('vote/', Voting.as_view(), name="vote"),
    path('primary/', PrimaryDate.as_view(), name="set primary"),
    path('event/leave/', LeaveEvent.as_view(), name="leave"),
    path('login/', Login.as_view(), name='login'),
    path('delete_notifications/', DeleteNotifications.as_view(), name='reject'),
    path('event/delete/', Delete.as_view(), name='delete')
]
