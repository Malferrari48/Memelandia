from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    utenteCreatore = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utenteCreatore",blank=True, null=True)
    utenteSecondo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utenteSecondo",blank=True, null=True)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)