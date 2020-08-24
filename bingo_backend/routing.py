from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url

from apps.core.consumers import GameConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url(r'auth/(?P<user_id>\w+)/$', GameConsumer),
    ])
})