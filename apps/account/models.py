from django.db import models

from apps.core.models import AbstratoModel


class Account(AbstratoModel):
    user = models.ForeignKey(to='auth_user.User', related_name='conta', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, default='')
    cpf = models.CharField(max_length=255, default='')
    conta = models.CharField(max_length=255)
    agencia = models.CharField(max_length=255)
    validade = models.CharField(max_length=144, blank=True, null=True)
    tipo = models.CharField(max_length=15, default='')
    banco = models.CharField(max_length=144, blank=True, null=True)


def __str__(self):
    return '{} - {} {}'.format(self.user.nick_name, self.agencia, self.conta)
