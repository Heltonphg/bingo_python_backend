import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import math

from django.utils import timezone

from apps.auth_user.models import User
from apps.core.models import Bingo
from apps.core.serializers import BingoSerializer
from apps.core.tread import ThredRegressive


class GlobalsConsumer(WebsocketConsumer):
    user_online = None
    bingo = None
    room_vip = None
    room_gratis = None

    def cancelOrReset(self, room):
        room.created_at = timezone.now()
        if len(room.users.all()) >= room.minumum_quantity:
            room.game_iniciado = True
        room.save()

    def calc_time(self, room):
        if room and not room.game_iniciado:
            limit_time = 50
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

    def atualizar_room(self, event):
        print("Att room!!!")
        self.send(json.dumps({'key': 'manager.att_room'}))

    def atualizar_room_prox(self, event):
        self.send(json.dumps({'key': 'manager.att_room_prox'}))

    def reload_bingo(self, event):
        bingo: Bingo = Bingo.objects.filter(id=event['bingo']['id']).first()
        self.send(json.dumps({'key': 'manager.att_bingo', 'value': BingoSerializer(instance=bingo).data}))

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'client.auth':
            print('o usuário {} se conectou'.format(request_dict['value']['nome']))
            self.send(json.dumps({'key': 'manager.verificarDispatch', 'value': ''}))
            self.getInfosBingo()
            thredRegressive = ThredRegressive()
            thredRegressive.start()
