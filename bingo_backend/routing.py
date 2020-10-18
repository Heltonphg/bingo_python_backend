from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url

from apps.core.consumers import GlobalsConsumer
from apps.core.gameconsumers import GameConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url(r'auth/(?P<user_id>\w+)/$', GlobalsConsumer),
        url(r'game/(?P<user_id>\w+)/(?P<room_id>\w+)/$', GameConsumer),
    ])
})