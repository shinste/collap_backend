from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class EventDate(models.Model):
    date = models.DateField(primary_key=True)
    def __str__(self):
        return str(self.date)
 
class Event(models.Model):
    # date = models.DateField()
    # date = models.ForeignKey(EventDates, on_delete=models.CASCADE)
    date = models.ManyToManyField(EventDate)
    name = models.CharField(max_length=100)
    # host = models.OneToManyField(User)
    date_created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    def participant_count(self):
        return self.participants.count()







# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.username
    
# # class EventDate(models.Model):
# #     date = models.DateField()
    
# #     def __str__(self):
# #         return str(self.date)
    
# class Event(models.Model):
#     # dates = models.ManyToManyField('EventDate', blank=True)
#     # host = 
#     name = models.CharField(max_length=100)
#     proposed_date = models.DateField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     participants = models.ManyToManyField(User)
#     num_participants = models.IntegerField(null=False, default=0)
#     def __str__(self):
#         return self.name
#     def participant_count(self):
#         return self.participants.count()
#     # def save(self, *args, **kwargs):
#     #     self.num_participants = self.participants.count()
#     #     super().save(*args, **kwargs)
# # def update_num_participants(sender, instance, **kwargs):
# #     instance.num_participants = instance.participants.count()
# #     instance.save()