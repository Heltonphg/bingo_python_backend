from django.db import models

from apps.users.models import User


class Event(models.Model):
    name = models.CharField(max_length=150)
    time_initiation = models.DateTimeField()
    is_activated = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    TYPES = [
        ("V", "Vip"),
        ("G", "Gratis")
    ]

    event = models.ForeignKey(Event, related_name="roons", on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField(User, related_name="roons", blank=True, null=True)
    type = models.CharField(max_length=1, choices=TYPES)
    premium_price = models.FloatField(default=0)
    initiation_game = models.DateTimeField(blank=True, null=True)
    minumum_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type
