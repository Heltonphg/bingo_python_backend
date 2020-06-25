from django.db import models

from apps.users.models import User


class Event(models.Model):
    name = models.CharField(max_length=150)
    is_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    event = models.ForeignKey(Event, related_name="roons", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="roons", blank=True)
    type = models.CharField(max_length=45)
    premium_price = models.FloatField()
    initiation_game = models.DateField()
    minumum_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type
