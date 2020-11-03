# from channels.routing import route
# from otree.channels.routing import channel_routing

# from cartelgame.consumers import ws_message, ws_add


# channel_routing += [
#     route("websocket.connect", ws_add, path=r"^/custom/report"),
#     route("websocket.receive", ws_message, path=r"^/custom/report"),
# ]

from channels.routing import route
# from otree.channels.routing import channel_routing

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url

from cartelgame.consumers import ws_message, ws_add

websocket_routes = [
    # url(r"^custom/report/", ws_add),
    # url(r"^custom/report/", ws_message),
    route("websocket.connect", ws_add, path=r"^/custom/report"),
    route("websocket.receive", ws_message, path=r"^/custom/report"),
]

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(websocket_routes))}
)