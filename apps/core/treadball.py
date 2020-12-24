import time, sys
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random

from apps.core.models import Room

GLOBAL_CHANNEL_LAYER = get_channel_layer()


class ThreadBall(Thread):
    group_name = None
    room = None
    kill = False

    def __init__(self, group_name, room):
        print(group_name, room)
        Thread.__init__(self)
        self.group_name = str(group_name)
        self.room = room
        self.kill = False

    def stoneSorted(self):
        position_sorted = random.randint(0, len(self.room.sorted_numbers) - 1)
        stone = self.room.sorted_numbers[position_sorted]
        return {'stone': stone, 'position': position_sorted}

    def run(self) -> None:
        while not self.kill:
            sys.stdout.flush()
            time.sleep(13)
            self.room = Room.objects.filter(pk=self.group_name).first()
            if self.room.finalized == True:
                print("++++++++Tentando encerrar++++++++++++")
                self.kill = True

            if self.kill == False:
                stone_sorted = self.stoneSorted()
                stone_sorted['stone']['sorted'] = True
                self.room.sorted_numbers[stone_sorted['position']] = stone_sorted['stone']

                new_numbers = list()
                for stone in self.room.sorted_numbers:
                    if stone['sorted'] == False:
                        new_numbers.append(stone)

            self.room.sorted_numbers = new_numbers
            self.room.save()


            async_to_sync(GLOBAL_CHANNEL_LAYER.group_send)(
                self.group_name,
                {'type': "sort.ball", 'value': stone_sorted['stone']['value']}
            )
