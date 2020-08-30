from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from bingo_backend import settings
from .managers import UserManager


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

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField('staff status', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{}'.format(self.full_name)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
