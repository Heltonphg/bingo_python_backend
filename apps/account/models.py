from django.db import models


class Account(models.Model):
    user = models.ForeignKey(to='auth_user.User', related_name='conta', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, default='')
    operacao = models.CharField(max_length=255)
    conta = models.CharField(max_length=255)
    agencia = models.CharField(max_length=255)
    validade = models.CharField(max_length=144, blank=True,
                                null=True)
    banco = models.CharField(max_length=144,blank=True,
                                null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} {}'.format(self.user.nick_name, self.agencia, self.conta)
