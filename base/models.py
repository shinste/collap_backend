from django.db import models
import random
import uuid


def generate_unique_id():
    
    while True:
        event_id = random.choices(range(10), k=6)
        if Event.objects.filter(event_id=event_id).count() == 0:
            break
    return event_id

class user(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username




class Event(models.Model):
    event_id = models.CharField(max_length=8, primary_key=True, default=uuid.uuid4, unique=True)
    primary_date = models.DateField()
    name = models.CharField(max_length=100)
    host = models.ForeignKey(user, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class EventDate(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, primary_key=True)
    date = models.DateField()
    
    class Meta:
        unique_together = ('event_id', 'date')

    def __str__(self):
        return str(self.event_id) + str(self.date)


class UserEvent(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(user, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event_id', 'username'], name='unique_userevent')
        ]

    # class Meta:
        unique_together = ('event_id', 'username')

    def __str__(self):
        return str(self.event_id) + str(self.username)

class Vote(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(user, on_delete=models.CASCADE)
    date = models.DateField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event_id', 'username'], name='unique_vote')
        ]

class Availability(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(user, on_delete=models.CASCADE)
    date = models.DateField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event_id', 'username', 'date'], name='unique_availability')
        ]

class Notification(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(user, on_delete=models.CASCADE)
    notification = models.CharField(max_length=500)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event_id', 'username', 'notification'], name='unique_notification')
        ]

    def __str__(self):
        return str(self.event_id) + str(self.username)

