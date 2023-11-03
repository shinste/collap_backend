from django.urls import path
from django.contrib import admin
from .views.getVotes import get_votes
from .views.joinEvent import JoinEvent
from .views.pushVote import PushVote

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/get_votes/', get_votes, name="get_votes"),
    path('event/join_event/', JoinEvent.as_view(), name="join_event"),
    path('event/push_vote/', PushVote.as_view(), name ="push_vote")
]
