from django.urls import path
from django.contrib import admin
from .views.viewEvents import *
from .views.getVotes import *
from .views.joinEvent import *
from .views.pushVote import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/view_events/', viewEvents, name='view_events'),
    path('event/get_votes/', getVotes, name="get_votes"),
    path('event/join_event/', joinEvent.as_view(), name="join_event"),
    path('event/push_vote/', pushVote.as_view(), name ="push_vote")
]
