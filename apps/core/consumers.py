import json
from django.dispatch import receiver
from django.db.models.signals import post_save

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import math
import time, sys

from django.utils import timezone

from apps.auth_user.models import User
from apps.card.models import CardBingo
from apps.core.models import Bingo, Room
from apps.notifications.models import Notifications


class GlobalsConsumer(WebsocketConsumer):
    user_online = None
    cartelao = None
    time = None
    bingo = None
    room_vip = None
    room_gratis = None

    def cancelOrReset(self, room):
        room.created_at = timezone.now()
        if len(room.users.all()) >= room.minumum_quantity:
            room.game_iniciado = True
        room.save()

    def calc_time(self, room):
        if room.game_iniciado == False:
            #todo: vai ser sete minutos
            limit_time = 500
            minutes = timezone.now() - room.created_at
            total_seconds = limit_time - minutes.total_seconds()
            if total_seconds <= 0:
                self.cancelOrReset(room)


            segundo = math.floor(total_seconds % 60)
            total_minutes = total_seconds / 60
            m = math.floor(total_minutes % 60)

            seconds = '0' + str(segundo) if segundo < 10 else segundo
            minutes = '0' + str(m) if m < 10 else m
            time = ''
            if total_seconds <= 0:
                time = '00:00'
            else:
                time = '{}:{}'.format(minutes, seconds)

            return time
        else:
            return 'Iniciado'

    def regressive_time(self, event):
        self.getInfosBingo()
        while True:
            comeco_vip = self.calc_time(self.room_vip)
            comeco_gratis = self.calc_time(self.room_gratis)

            # if comeco_vip or comeco_vip == '09:00':
            #     notifica = Notifications.objects.filter(user=self.user_online, lida=False).first()
            #     if not notifica:
            #         Notifications.objects.create(user=self.user_online,
            #                                      message="O jogo vai começar em {} minutos".format(comeco),
            #                                      title="Depressa, faltam {} minutos!!!".format(comeco))
            #         self.send(json.dumps({'key': 'manager.notificas', 'value': ''}))

            self.send(json.dumps({'key': 'manager.regressive_vip', 'value': comeco_vip}))
            self.send(json.dumps({'key': 'manager.regressive_gratis', 'value': comeco_gratis}))
            sys.stdout.flush()
            time.sleep(1)

    def getInfosBingo(self):
        if not self.bingo:
            if Bingo.objects.filter(is_activated=True).exists():
                self.bingo = Bingo.objects.filter(is_activated=True).first()
                self.room_vip = self.bingo.rooms.all().get(type='Vip')
                self.room_gratis = self.bingo.rooms.all().get(type='Grátis')

    def connect(self):
        id = self.scope['url_route']['kwargs']['user_id']
        self.getInfosBingo()

        self.user_online = User.objects.filter(pk=id).first()

        if CardBingo.objects.filter(is_activate=True, user=self.user_online).exists():
            self.cartelao = CardBingo.objects.filter(is_activate=True, user=self.user_online).first()
        if not self.user_online:
            self.close()
        async_to_sync(self.channel_layer.group_add)("globals", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'client.auth':
            print('o usuário {} se conectou'.format(request_dict['value']['nome']))
            self.send(json.dumps({'key': 'manager.teste', 'value': ''}))
            async_to_sync(self.channel_layer.group_send)(
                'globals',
                {'type': "regressive.time"}
            )

            if self.cartelao:
                self.send(json.dumps({'key': 'manager.cartelao', 'value': self.cartelao.cartelao}))

        if request_dict['key'] == 'log':
            print(request_dict['value']['message'])


@receiver(post_save, sender=Bingo)
def pos_save(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'globals',
            {
                'type': "regressive.time",
            }
        )
