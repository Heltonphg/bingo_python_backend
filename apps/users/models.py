import jsonfield
from django.db import models
from cpffield import cpffield


class User(models.Model):
    SEX = [
        ("M", "Masculino"),
        ("F", "Feminino")
    ]
    email = models.EmailField()
    password = models.CharField(max_length=45)
    full_name = models.CharField(max_length=144)
    nick_name = models.CharField(max_length=144, unique=True)
    cpf = cpffield.CPFField('CPF', max_length=14)
    phone = models.CharField(max_length=22)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)
    avatar = models.ImageField(upload_to='images', verbose_name='Imagem', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class CardBingo(models.Model):
    TYPES = [
        ("V", "Vip"),
        ("G", "Gratis")
    ]
    user = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE)
    card = jsonfield.JSONField()
    is_activate = models.BooleanField(default=False)
    price = models.FloatField()
    type = models.CharField(max_length=1, choices=TYPES)

    def __str__(self):
        return "{} - {}".format(self.user.full_name, self.type)
