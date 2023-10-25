from django.urls import path
from .views import *
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.Homepage, name="homepage"),
    path('admin/', admin.site.urls),
    path('event/view/', EventView.as_view(), name="event"),
    path('notification/', views.notificationView , name="notifications"),
    path('user/view_events/', views.viewEvents, name='view_events'),
    path('event/get_votes/', views.getVotes, name="get_votes"),
    path('event/join_event/', joinEvent.as_view(), name="join_event"),
    path('event/push_vote/', pushVote.as_view(), name ="push_vote")
]
