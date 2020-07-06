import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from apps.auth_user.models import User


class AppConsumer(WebsocketConsumer):
    user_online = None

    def connect(self):
        id = self.scope['url_route']['kwargs']['user_id']
        print(id)
        self.user_online = User.objects.filter(pk=id).first()
        if not self.user_online:
            self.close()
        # async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass
        # if self.user_online:
        #     async_to_sync(self.user_online.delete())
            # async_to_sync(self.channel_layer.group_discard)(
            #     self.room_group_name,
            #     self.channel_name
            # )

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)

        if request_dict['key'] == 'anviar.aviso':
            print(request_dict['value']['message'])
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
