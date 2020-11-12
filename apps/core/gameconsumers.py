import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from apps.auth_user.models import User
from apps.card.models import CardBingo
from apps.core.models import Room
from apps.core.treadball import ThreadBall


class GameConsumer(WebsocketConsumer):
    user_game = None
    cartelao = None
    group = None
    room = None

    def connect(self):
        id = self.scope['url_route']['kwargs']['user_id']
        self.group = self.scope['url_route']['kwargs']['room_id']

        self.user_game = User.objects.filter(pk=id).first()
        self.room = Room.objects.filter(pk=self.group).first()

        if not self.user_game:
            self.close()

        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.channel_name, self.group)

    def sort_ball(self, event):
        self.send_att_warning(event['value'])
        self.send(json.dumps({'key': 'game.sort', 'value': '{}'.format(event['value'])}))

    def get_position_card(self, stone_value):
        for i, tupla in enumerate(self.cartelao.cartelao['cartela'], start=0):
            for j, stone in enumerate(tupla, start=0):
                if stone_value == stone['value']:
                    return {'i': i, 'j': j}

    def send_att_card(self, stone_value):
        postion = self.get_position_card(stone_value)
        if self.cartelao.cartelao['cartela'][postion['i']][postion['j']]['marked'] == True:
            self.cartelao.cartelao['cartela'][postion['i']][postion['j']]['marked'] = False
        else:
            self.cartelao.cartelao['cartela'][postion['i']][postion['j']]['marked'] = True
        self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))
        self.cartelao.save()

    def send_att_warning(self, stone_value):
        postion = self.get_position_card(str(stone_value))
        if self.cartelao.cartelao['cartela'][postion['i']][postion['j']]['warning'] == False:
            self.cartelao.cartelao['cartela'][postion['i']][postion['j']]['warning'] = True
            self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))
            self.cartelao.save()


    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'user.game':
            print('o usuário {} se conectou na sala {}'.format(request_dict['value']['nome'], self.group))
            if not self.cartelao:
                self.cartelao = CardBingo.objects.filter(user=self.user_game).first()
            thredBall = ThreadBall(group_name=self.room.id, room=self.room)
            thredBall.start()

        if request_dict['key'] == 'marker_stone':
            self.send_att_card(request_dict['value']['object']['value'])
