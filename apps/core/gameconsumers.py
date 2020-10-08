import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from apps.auth_user.models import User


class GameConsumer(WebsocketConsumer):
    user_game = None

    def connect(self):
        id = self.scope['url_route']['kwargs']['user_id']
        self.user_game = User.objects.filter(pk=id).first()

        if not self.user_game:
            self.close()
        async_to_sync(self.channel_layer.group_add)("game", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'user.game':
            print('o usuário {} se conectou na sala'.format(request_dict['value']['nome']))
