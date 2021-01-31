from django.db import models
from django.contrib.postgres.fields import JSONField

from apps.core.models import AbstratoModel


class CardBingo(AbstratoModel):
    user = models.ForeignKey(to='auth_user.User', related_name="cards", on_delete=models.CASCADE)
    room = models.ForeignKey(to='core.Room', related_name="cards", on_delete=models.SET_NULL, blank=True, null=True)
    cartelao = JSONField(null=True, blank=True)
    is_activate = models.BooleanField(default=True)
    price = models.FloatField()

    def __str__(self):
        return '{} - {}'.format(self.user.full_name, self.is_activate)
