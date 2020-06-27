import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from apps.users.models import User


class AppConsumer(WebsocketConsumer):
    user_online = None

    def connect(self):
        # print("deda",self.scope['url_route']['kwargs']['user_id'])
        # self.user_online = User.objects.filter(user_id=1)
        # if not self.user_online:
        #     self.close()
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
