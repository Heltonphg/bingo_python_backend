from django.db import models, transaction


class Bingo(models.Model):
    name = models.CharField(max_length=150)
    is_activated = models.BooleanField(default=True)
    is_prox_stack = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if Bingo.objects.filter(is_activated=True).first():
            if not self.pk:
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
    minumum_quantity = models.IntegerField()
    attempts = models.IntegerField(default=3)
    game_iniciado = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    value_card = models.FloatField()
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
