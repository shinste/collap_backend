from django.contrib import admin
from .models import Event, user, EventDate, EventUser, Vote, Notification, Availability
# Register your models here.


admin.site.register(Event)

admin.site.register(user)

admin.site.register(EventDate)

admin.site.register(EventUser)

admin.site.register(Vote)

admin.site.register(Notification)

admin.site.register(Availability)