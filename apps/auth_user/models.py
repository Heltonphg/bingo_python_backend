from django.core import serializers
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .managers import UserManager
from ..core.models import AbstratoModel


class User(AbstractBaseUser, PermissionsMixin):
    MASCULINO = 'MASCULINO'
    FEMININO = 'FEMININO'
    SEX = [
        (MASCULINO, "Masculino"),
        (FEMININO, "Feminino")
    ]
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=144)
    nick_name = models.CharField(max_length=144)
    cpf = models.CharField('CPF', max_length=14)
    phone = models.CharField(max_length=22)
    sex = models.CharField(max_length=10, choices=SEX)
    avatar = models.ImageField(upload_to='images', verbose_name='Imagem', null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    token = models.CharField(max_length=22, null=True, blank=True, default=None)
    token_created_at = models.DateField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    token_notification = models.TextField(default='', null=True, blank=True)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField('staff status', default=False)

    @property
    def valor_para_receber(self):
        valor = 0
        for win in self.wins.all():
            valor += win.price
        return valor


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    def __str__(self):
        return '{}'.format(self.full_name)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')



class Vitoria(AbstratoModel):
    user = models.ForeignKey(to='auth_user.User', related_name="wins", on_delete=models.CASCADE)
    room = models.ForeignKey(to='core.Room', related_name="user_wins", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_pago = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'room')

    def __str__(self):
        return "{} ganhou {} ".format(self.user.nick_name, self.price)

    def save(self, *args, **kwargs):
        vitorioso = Vitoria.objects.filter(room__type="Vip").first()
        if vitorioso and vitorioso.user.pk != self.user.pk:
            raise serializers.ValidationError('Só é permitido um jogador ganahr!')
        return super(Vitoria, self).save(*args, **kwargs)
