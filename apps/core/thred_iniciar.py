import time, sys
from threading import Thread
from channels.layers import get_channel_layer

from apps.core.models import Bingo, Room
from apps.core.treadball import ThreadBall

GLOBAL_CHANNEL_LAYER = get_channel_layer()

class ThredVerifica(Thread):
    def run(self) -> None:
        print("Verificando se iniciou")
        vip = False
        gratis = False
        while True:
            bingo = Bingo.objects.filter(is_activated=True).first()
            if bingo:
                for room in bingo.rooms.all():
                    if vip == False and room.type == 'Vip' and room.game_iniciado == True:
                        print("A sala {} foi iniciado".format(room.id))
                        vip = True
                        thredBall = ThreadBall(group_name=room.id,room=room)
                        thredBall.start()
                    if gratis == False and room.type == 'Grátis' and room.game_iniciado == True:
                        print("A sala {} foi iniciado".format(room.id))
                        gratis = True
                        thredBall = ThreadBall(group_name=room.id, room=room)
                        thredBall.start()
            else:
                pass
            sys.stdout.flush()
            time.sleep(5)