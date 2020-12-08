import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from apps.auth_user.models import User
from apps.auth_user.serializers import UserSimpleSerializer
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

    def user_win(self, event):
        self.room.finalized = True
        self.room.save()
        self.send(json.dumps({'key': 'game.user_win', 'value': UserSimpleSerializer(instance=self.user_game).data}))

    def get_position_card(self, stone_value):
        for i, tupla in enumerate(self.cartelao.cartelao['cartela'], start=0):
            for j, stone in enumerate(tupla, start=0):
                if stone_value == stone['value']:
                    return {'i': i, 'j': j}

    def sort_ball(self, event):
        position = self.get_position_card(str(event['value']))
        counter_warning = 1
        for stone in self.cartelao.cartelao['cartela'][position['i']]:
            if stone['value'] != '*' and stone['warning'] == True:
                counter_warning += 1
        if counter_warning <= 4:
            self.send_att_warning(event['value'])
            self.send(json.dumps({'key': 'game.sortspeaker', 'value': '{}'.format(event['value'])}))
        else:
            self.send(json.dumps({'key': 'game.sortspeaker', 'value': '{}'.format(event['value'])}))
            self.send_att_beaten(event['value'])
        self.room = Room.objects.filter(pk=self.group).first() #todo:preciso atualizar a minha sala para que sempre as sorted_numbers estejam atualizadas!

    def is_present_in_sorted_numbers(self, stone_marker):
        for stone in self.room.sorted_numbers:
            if str(stone['value']) == str(stone_marker['value']):
                return False
        return True

    def marker_stone_send(self, stone_value):
        position = self.get_position_card(stone_value)
        if self.cartelao.cartelao['cartela'][position['i']][position['j']]['beaten'] == True:
            self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] = True
            async_to_sync(self.channel_layer.group_send)(
                self.group,
                {'type': "user.win", 'value': self.cartelao.cartelao['cartela'][position['i']][position['j']]['value']}
            )
        else:
            if self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] == True:
                self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] = False
            else:
                print("OQ RETORNA:", self.is_present_in_sorted_numbers(
                    stone_marker=self.cartelao.cartelao['cartela'][position['i']][position['j']]))
                if self.is_present_in_sorted_numbers(
                        stone_marker=self.cartelao.cartelao['cartela'][position['i']][position['j']]):
                    self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] = True
                else:
                    print('Não pode marcar pq nao foi sorteado')
        self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))
        self.cartelao.save()

    def send_att_beaten(self, stone_value):
        position = self.get_position_card(str(stone_value))
        if self.cartelao.cartelao['cartela'][position['i']][position['j']]['beaten'] == False:
            self.cartelao.cartelao['cartela'][position['i']][position['j']]['beaten'] = True
            self.cartelao.save()
            self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))


    def send_att_warning(self, stone_value):
        position = self.get_position_card(str(stone_value))
        if self.cartelao.cartelao['cartela'][position['i']][position['j']]['warning'] == False:
            self.cartelao.cartelao['cartela'][position['i']][position['j']]['warning'] = True
            self.cartelao.save()
            self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))


    def atualizar_cartelao(self):
        self.cartelao = CardBingo.objects.filter(user=self.user_game).first()

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'user.game':
            print('o usuário {} se conectou na sala {}'.format(request_dict['value']['nome'], self.group))
            if not self.cartelao:
                self.atualizar_cartelao()
            # thredBall = ThreadBall(group_name=self.room.id, room=self.room)
            # thredBall.start()

        if request_dict['key'] == 'marker_stone':
            self.marker_stone_send(request_dict['value']['object']['value'])
