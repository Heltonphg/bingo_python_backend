from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from cpffield import cpffield
from .managers import UserManager
from django.contrib.auth.hashers import make_password


class User(AbstractBaseUser, PermissionsMixin):
    SEX = [
        ("M", "Masculino"),
        ("F", "Feminino")
    ]
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=144)
    nick_name = models.CharField(max_length=144)
    cpf = models.CharField('CPF', max_length=14)
    phone = models.CharField(max_length=22)
    birth_date = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX)
    avatar = models.ImageField(upload_to='images', verbose_name='Imagem', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

