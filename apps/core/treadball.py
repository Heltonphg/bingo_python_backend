import time, sys
from random import randrange
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

GLOBAL_CHANNEL_LAYER = get_channel_layer()


class TreadBall(Thread):
    group_name = None
    room = None
    sorted_numbers = []
    def __init__(self, group_name, room):
        Thread.__init__(self)
        self.group_name = group_name
        self.room = room
        self.sorted_numbers = room.sorted_numbers

    def run(self) -> None:
        print("AQUII", type(self.sorted_numbers))
        while True:
            sys.stdout.flush()
            time.sleep(5)
            async_to_sync(GLOBAL_CHANNEL_LAYER.group_send)(
                self.group_name,
                {'type': "sort.ball", 'valor': 2 }
            )

