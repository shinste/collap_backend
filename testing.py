import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collap.settings")
django.setup()
from base.models import Event, User


a1 = Event(name='Activity1', proposed_date='2023-09-10')
# print(a1)
a1.participants.add('joseph')
a1.participants.add('kendrick')
print(a1.participants)