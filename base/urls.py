from django.urls import path
from .views.createevent import CreateEvent
from .views.delete import Delete
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
from .views.joinevent import JoinEvent
from .views.geteventinfo import GetEventInfo
from .views.eventdates import EventDates
from .views.invite import Invite
from .views.getvotes import GetVotes
from .views.pushvote import PushVote
from .views.editdate import EditDate
from .views.changeprimary import ChangePrimary
from .views.getcsrftoken import get_csrf_view
from .views.homepage import Homepage
from django.contrib import admin


urlpatterns = [
    # path('', admin.site.urls, name="homepage"),
    # path('/admin', admin.site.urls, name="admin"),
    path('event/view/', ViewEvents.as_view(), name="event view"),
    path('notification/', NotificationView.as_view() , name="notifications"),
    path('register/', Register.as_view(), name="register"),
    path('event/hosted/', HostedEvents.as_view(), name="hosted events"),
    path('ranked/', RankDates.as_view(), name="rank"),
    path('event/create/', CreateEvent.as_view(), name="create event"),
    path('vote/', Voting.as_view(), name="vote"),
    # path('primary/', PrimaryDate.as_view(), name="set primary"),
    path('event/leave/', LeaveEvent.as_view(), name="leave"),
    path('login/', Login.as_view(), name='login'),
    path('delete_notifications/', DeleteNotifications.as_view(), name='reject'),
    path('event/delete/', Delete.as_view(), name='delete'), 
    path('event/join/', JoinEvent.as_view(), name="join_event"),
    path('event/get_info/', GetEventInfo.as_view(), name="get event info"),
    path('event/dates/', EventDates.as_view(), name="get event info"),
    path('event/invite/', Invite.as_view(), name="invite"),
    path('event/get_votes/', GetVotes.as_view(), name="get votes"),
    path('event/push_votes/', PushVote.as_view(), name="push votes"),
    path('event/edit_date/', EditDate.as_view(), name="edit date"),
    path('event/change_primary/', ChangePrimary.as_view(), name="change primary date"),
    path('get-csrf-token/', get_csrf_view.as_view(), name='get_csrf_token'),
    path('', admin.site.urls, name="homepage"),
]
