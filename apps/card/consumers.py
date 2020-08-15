import json
import asyncio
from background_task import background
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from apps.auth_user.models import User
from apps.card.models import CardBingo

class GlobalConsumer(WebsocketConsumer):
    user_online = None
    catelao = None

    def regressive_time(self, event):
        self.send(json.dumps({'key': 'manager.regressive', 'value': 'kiko'}))

    def connect(self):
        id = self.scope['url_route']['kwargs']['user_id']
        self.user_online = User.objects.filter(pk=id).first()
        catelao = CardBingo.objects.filter(is_activate=True, user=self.user_online).first()
        if catelao:
            self.catelao = catelao
        if not self.user_online:
            self.close()
        async_to_sync(self.channel_layer.group_add)("global", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'client.auth':
            async_to_sync(self.channel_layer.group_send)(
                'global',
                {'type': "regressive.time"}
            )
            self.send(json.dumps({'key': 'manager.cartela', 'value': self.catelao.cartelao}))

        if request_dict['key'] == 'log':
            print(request_dict['value']['message'])

