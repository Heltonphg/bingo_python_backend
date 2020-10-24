import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from random import randrange
from apps.auth_user.models import User
from apps.core.treadball import TreadBall


class GameConsumer(WebsocketConsumer):
    user_game = None
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
        # self.close()

    def sort_ball(self, event):
        self.send(json.dumps({'key': 'game.sort', 'value': '{}'.format(randrange(0, 90))}))

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'user.game':
            print('o usuário {} se conectou na sala {}'.format(request_dict['value']['nome'],self.group))
            tread_ball = TreadBall()
            tread_ball.start()
