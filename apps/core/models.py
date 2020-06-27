from django.db import models
from apps.users.models import User


class Event(models.Model):
    name = models.CharField(max_length=150)
    is_activated = models.BooleanField(default=True)
    time_initiation = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.time_initiation.strftime('%b/%d/%Y (%A) as %H:%M:%S '))


class Room(models.Model):
    TYPES = [
        ("V", "Vip"),
        ("G", "Gratis")
    ]
    event = models.ForeignKey(Event, related_name="roons", on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField(User, related_name="roons", blank=True, default=list)
    type = models.CharField(max_length=1, choices=TYPES)
    premium_price = models.FloatField(default=0)
    minumum_quantity = models.IntegerField()
    initiation_game = models.DateTimeField(blank=True, null=True)
    value_card = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type
