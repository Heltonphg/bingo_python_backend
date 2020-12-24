import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.db import transaction

from apps.auth_user.models import User, Vitoria
from apps.auth_user.serializers import UserSimpleSerializer
from apps.card.models import CardBingo
from apps.core.models import Room
from apps.notifications.models import Notifications


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
        with transaction.atomic():
            self.room = Room.objects.filter(pk=self.group).first()
            self.room.finalized = True
            self.send(json.dumps({'key': 'game.user_win', 'value': event['value']}))

            if event['value']['id'] == self.user_game.id:
                Vitoria.objects.create(user_id=event['value']['id'], room_id=self.group, price=self.room.valor_premio)
                Notifications.objects.create(user_id=event['value']['id'], title="Parabéns",
                                             message="Você foi o vencedor do bingo {}. Seu prêmio foi no valor de {}".format(
                                                 self.group, self.room.valor_premio))
            self.room.save()

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
                {'type': "user.win", 'value': UserSimpleSerializer(instance=self.user_game).data}
            )
        else:
            if self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] == True:
                self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] = False
                print("Desmarcado")
            else:
                print("OQ RETORNA:", self.is_present_in_sorted_numbers(
                    stone_marker=self.cartelao.cartelao['cartela'][position['i']][position['j']]))
                if self.is_present_in_sorted_numbers(
                        stone_marker=self.cartelao.cartelao['cartela'][position['i']][position['j']]):
                    self.cartelao.cartelao['cartela'][position['i']][position['j']]['marked'] = True
                else:
                    print('Não pode marcar pq nao foi sorteado')
        self.cartelao.save()
        self.atualizar_cartelao()
        self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))

    def send_att_beaten(self, stone_value):
        position = self.get_position_card(str(stone_value))
        if self.cartelao.cartelao['cartela'][position['i']][position['j']]['beaten'] == False:
            self.cartelao.cartelao['cartela'][position['i']][position['j']]['beaten'] = True
            self.cartelao.save()
            self.atualizar_cartelao()
            self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))

    def send_att_warning(self, stone_value):
        position = self.get_position_card(str(stone_value))
        if self.cartelao.cartelao['cartela'][position['i']][position['j']]['warning'] == False:
            self.cartelao.cartelao['cartela'][position['i']][position['j']]['warning'] = True
            self.cartelao.save()
            self.atualizar_cartelao()
            self.send(json.dumps({'key': 'game.att_cartelao', 'value': self.cartelao.cartelao['cartela']}))

    def atualizar_cartelao(self):
        self.cartelao = CardBingo.objects.filter(user=self.user_game).first()

    def receive(self, text_data=None, bytes_data=None):
        request_dict = json.loads(text_data)
        if request_dict['key'] == 'user.game':
            print('o usuário {} se conectou na sala {}'.format(request_dict['value']['nome'], self.group))
            if not self.cartelao:
                self.atualizar_cartelao()

        if request_dict['key'] == 'marker_stone':
            self.marker_stone_send(request_dict['value']['object']['value'])
