import jsonfield
from django.db import models

class CardBingo(models.Model):
    user = models.ForeignKey(to='auth_user.User', related_name="cards", on_delete=models.CASCADE)
    room = models.ForeignKey(to='core.Room', related_name="cards", on_delete=models.SET_NULL, blank=True, null=True)
    card = jsonfield.JSONField()
    is_activate = models.BooleanField(default=False)
    price = models.FloatField()

    def __str__(self):
        return "{}".format(self.user.full_name)
