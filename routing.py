from channels.routing import route
from otree.channels.routing import channel_routing

from cartelgame.consumers import ws_message, ws_add


channel_routing += [
    route("websocket.connect", ws_add, path=r"^/custom/report"),
    route("websocket.receive", ws_message, path=r"^/custom/report"),
]
