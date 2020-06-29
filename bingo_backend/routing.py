from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url

from apps.users.consumers import AppConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url(r'auth/(?P<user_id>\w+)/$', AppConsumer),
    ])
})