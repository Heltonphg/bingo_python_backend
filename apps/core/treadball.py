import time, sys
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random

GLOBAL_CHANNEL_LAYER = get_channel_layer()


class ThreadBall(Thread):
    group_name = None
    room = None
    sorted_numbers = []
    kill = False

    def __init__(self, group_name, room):
        print(group_name,room)
        Thread.__init__(self)
        self.group_name = str(group_name)
        self.room = room
        self.sorted_numbers = room.sorted_numbers

    def stoneSorted(self):
        stone_sorted = random.randint(0, len(self.sorted_numbers)-1)
        stone = self.sorted_numbers[stone_sorted]
        return {'stone': stone, 'position': stone_sorted}

    def run(self) -> None:
        self.kill = False
        while not self.kill:
            if self.room.finalized == True:
                print("Bug em Encerrar-----------")
                self.kill = True
            sys.stdout.flush()
            time.sleep(20)
            stone_sorted = self.stoneSorted()
            stone_sorted['stone']['sorted'] = True
            self.room.sorted_numbers[stone_sorted['position']] = stone_sorted['stone']
            new_numbers = list()
            for stone in self.sorted_numbers:
                if stone['sorted'] == False:
                    new_numbers.append(stone)
            self.sorted_numbers = new_numbers
            self.room.sorted_numbers = new_numbers
            self.room.save()
            if len(self.sorted_numbers) == 0:
                self.kill = True

            async_to_sync(GLOBAL_CHANNEL_LAYER.group_send)(
                self.group_name,
                {'type': "sort.ball", 'value': stone_sorted['stone']['value']}
            )

