import json
from django.dispatch import receiver
from django.db.models.signals import post_save

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import math

from django.utils import timezone

from apps.auth_user.models import User
from apps.core.models import Bingo
from apps.core.serializers import RoomSerializer, BingoSerializer
from apps.core.tread import MyTread


class GlobalsConsumer(WebsocketConsumer):
    user_online = None
    time = None
    bingo = None
    room_vip = None
    room_gratis = None

    def cancelOrReset(self, room):
        room.created_at = timezone.now()
        if len(room.users.all()) >= room.minumum_quantity:
            room.game_iniciado = True
            room.closed = True
        room.save()

    def calc_time(self, room):
        if room and not room.game_iniciado and not room.closed:
            limit_time = 420
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
        if not self.bingo:
            self.getInfosBingo()
        comeco_vip = self.calc_time(self.room_vip)
        comeco_gratis = self.calc_time(self.room_gratis)
        self.send(json.dumps({'key': 'manager.regressive_vip', 'value': comeco_vip}))
        self.send(json.dumps({'key': 'manager.regressive_gratis', 'value': comeco_gratis}))

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

        if not self.user_online:
            self.close()
        async_to_sync(self.channel_layer.group_add)("globals", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.channel_name, 'globals')
        # self.close()

    def atualizar_room(self, event):
        print('atualizar_room')
        self.send(json.dumps({'key': 'manager.att_room', 'value': event['room']}))

    def reload_bingo(self, event):
        t = MyTread()
        t.start()
        self.send(json.dumps({'key': 'manager.att_bingo', 'value': event['bingo']}))

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'client.auth':
            print('o usuário {} se conectou'.format(request_dict['value']['nome']))
            self.send(json.dumps({'key': 'manager.verificarDispatch', 'value': ''}))
            self.getInfosBingo()
            t = MyTread()
            t.start()

        if request_dict['key'] == 'log':
            print(request_dict['value']['message'])


@receiver(post_save, sender=Bingo)
def pos_save(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'globals',
            {
                'type': "reload.bingo",
                 'bingo': BingoSerializer(instance=instance).data
            }
        )
