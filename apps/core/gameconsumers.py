import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from random import randrange
from apps.auth_user.models import User
from apps.card.models import CardBingo
from apps.core.treadball import TreadBall


class GameConsumer(WebsocketConsumer):
    user_game = None
    cartelao = None
    group = None

    def connect(self):
        id = self.scope['url_route']['kwargs']['user_id']
        self.group = self.scope['url_route']['kwargs']['room_id']
        self.user_game = User.objects.filter(pk=id).first()
        if not self.user_game:
            self.close()
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.channel_name, self.group)

    def sort_ball(self, event):
        self.send(json.dumps({'key': 'game.sort', 'value': '{}'.format(randrange(0, 90))}))

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'user.game':
            print('o usuário {} se conectou na sala {}'.format(request_dict['value']['nome'], self.group))
            if not self.cartelao:
                self.cartelao = request_dict['value']['cartelao']
            # tread_ball = TreadBall()
            # tread_ball.start()

        if request_dict['key'] == 'marker_stone':
            for i, tupla in enumerate(self.cartelao, start=0):
                for j, stone in enumerate(tupla, start=0):
                    if request_dict['value']['object'] == stone:
                        self.cartelao[i][j]['marked'] = True
            self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao}))

