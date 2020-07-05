from django.db import models, transaction
from rest_framework import serializers

from apps.users.models import User


class Bingo(models.Model):
    name = models.CharField(max_length=150)
    is_activated = models.BooleanField(default=True)
    time_initiation = models.DateTimeField()

    def save(self, *args, **kwargs):
        if Bingo.objects.filter(is_activated=True).first():
            raise serializers.ValidationError('Já existe um bingo ativo')
        else:
            with transaction.atomic():
                super(Bingo, self).save(*args, **kwargs)
                Room.objects.create(bingo_id=self.id, minumum_quantity=10, type='Vip', value_card=2)
                Room.objects.create(bingo_id=self.id, minumum_quantity=5, type='Grátis', value_card=0)



    def __str__(self):
        return '{} - {}'.format(self.name, self.time_initiation.strftime('%b/%d/%Y (%A) as %H:%M:%S '))


class Room(models.Model):
    TYPES = [
        ("Vip", "Vip"),
        ("Grátis", "Grátis")
    ]
    bingo = models.ForeignKey(to='Bingo', related_name="rooms", on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField(User, related_name="rooms", blank=True, default=list)
    type = models.CharField(max_length=10, choices=TYPES)
    premium_price = models.FloatField(default=0)
    minumum_quantity = models.IntegerField()
    initiation_game = models.DateTimeField(blank=True, null=True)
    value_card = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_pode_entrar(self, card):
        return card.is_activate and self.id == card.room_id

    def __str__(self):
        return self.type
