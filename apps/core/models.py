from django.db import models, transaction
from rest_framework import serializers
from django.contrib.postgres.fields import JSONField


class Bingo(models.Model):
    name = models.CharField(max_length=150)
    is_activated = models.BooleanField(default=True)
    is_prox_stack = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if Bingo.objects.filter(is_activated=True).first():
            if not self.pk:
                if Bingo.objects.filter(is_prox_stack=True).first():
                    raise serializers.ValidationError('O próximo bingo já foi criado')
                else:
                    with transaction.atomic():
                        self.is_activated = False
                        self.is_prox_stack = True
                        super(Bingo, self).save(*args, **kwargs)
                        Room.objects.create(bingo_id=self.id, minumum_quantity=10, type='Vip', value_card=7)
                        Room.objects.create(bingo_id=self.id, minumum_quantity=5, type='Grátis', value_card=0)
            else:
                super(Bingo, self).save(*args, **kwargs)
        else:
            with transaction.atomic():
                super(Bingo, self).save(*args, **kwargs)
                Room.objects.create(bingo_id=self.id, minumum_quantity=2, type='Vip', value_card=7)
                Room.objects.create(bingo_id=self.id, minumum_quantity=1, type='Grátis', value_card=0)

    def __str__(self):
        return '{} - {}'.format(self.name, self.created_at.strftime('%b/%d/%Y (%A) as %H:%M:%S '))


class Room(models.Model):
    TYPES = [
        ("Vip", "Vip"),
        ("Grátis", "Grátis")
    ]
    bingo = models.ForeignKey(to='Bingo', related_name="rooms", on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField(to='auth_user.User', related_name="rooms", blank=True, default=list)
    type = models.CharField(max_length=10, choices=TYPES)
    game_iniciado = models.BooleanField(default=False)
    value_card = models.FloatField()
    minumum_quantity = models.IntegerField()
    sorted_numbers = JSONField(default=[
        {'value': 1, 'sorted': False},
        {'value': 2, 'sorted': False},
        {'value': 3, 'sorted': False},
        {'value': 4, 'sorted': False},
        {'value': 5, 'sorted': False},
        {'value': 6, 'sorted': False},
        {'value': 7, 'sorted': False},
        {'value': 8, 'sorted': False},
        {'value': 9, 'sorted': False},
        {'value': 10, 'sorted': False},
        {'value': 11, 'sorted': False},
        {'value': 12, 'sorted': False},
        {'value': 13, 'sorted': False},
        {'value': 14, 'sorted': False},
        {'value': 15, 'sorted': False},
        {'value': 16, 'sorted': False},
        {'value': 17, 'sorted': False},
        {'value': 18, 'sorted': False},
        {'value': 19, 'sorted': False},
        {'value': 20, 'sorted': False},
        {'value': 21, 'sorted': False},
        {'value': 22, 'sorted': False},
        {'value': 23, 'sorted': False},
        {'value': 24, 'sorted': False},
        {'value': 25, 'sorted': False},
    ])

    finalized = models.BooleanField(default=False)
    attempts = models.IntegerField(default=3)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_pode_entrar(self, card):
        return card.is_activate and self.id == card.room_id

    @property
    def valor_premio(self):
        valor = 0
        for users in self.users.all():
            for card in users.cards.all():
                if card.is_activate:
                    valor += card.price
        return valor

    class Meta:
        ordering = ['-value_card']

    def __str__(self):
        return self.type
