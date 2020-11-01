import time, sys
from random import randrange
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

GLOBAL_CHANNEL_LAYER = get_channel_layer()


class TreadBall(Thread):
    # group_name = None
    # def __init__(self, group_name):
    #     self.group_name = group_name

    def run(self) -> None:
        while True:
            sys.stdout.flush()
            time.sleep(20)
            number = randrange(0, 90)
            async_to_sync(GLOBAL_CHANNEL_LAYER.group_send)(
                '145',
                {'type': "sort.ball", 'valor': number }
            )

