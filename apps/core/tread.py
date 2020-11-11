import time, sys
from threading import Thread
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

GLOBAL_CHANNEL_LAYER = get_channel_layer()


class ThredRegressive(Thread):
    def run(self) -> None:
        while True:
            async_to_sync(GLOBAL_CHANNEL_LAYER.group_send)(
                'globals',
                {'type': "regressive.time"}
            )
            sys.stdout.flush()
            time.sleep(1)
