from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateField()
    end = models.DateField()
    location = models.CharField(max_length=255) #maybe fetch 
    limit = models.IntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tickets = models.IntegerField()

    def __str__(self):
        return self.event.name
