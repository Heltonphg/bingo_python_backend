import time, sys
from threading import Thread
from channels.layers import get_channel_layer

from apps.core.models import Bingo, Room
from apps.core.treadball import ThreadBall

GLOBAL_CHANNEL_LAYER = get_channel_layer()

class ThredVerifica(Thread):
    pode_verificar = True
    def run(self) -> None:
        while True:
            bingo = Bingo.objects.filter(is_activated=True).first()

            if bingo:
                for room2 in bingo.rooms.all():
                    if room2.type == 'Vip':
                        if room2.game_iniciado == False:
                            self.pode_verificar = True


                if self.pode_verificar:
                    print("Verificando se iniciou {}-{}".format(bingo.pk, bingo.is_activated))
                    for room in bingo.rooms.all():
                        if room.type == 'Vip':
                            print(room.game_iniciado)

                        if room.type == 'Vip' and room.game_iniciado == True:
                            print("A sala {} foi iniciado".format(room.id))
                            thredBall = ThreadBall(group_name=room.id, room=room)
                            thredBall.start()
                            self.pode_verificar = False
            else:
                pass
            sys.stdout.flush()
            time.sleep(5)