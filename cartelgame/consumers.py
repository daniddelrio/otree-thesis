import json
import time

from django.http import HttpResponse
from channels.handler import AsgiHandler

from otree.models import Participant, Session
from .models import Player


def ws_add(message):
    message.reply_channel.send({
        "text": "connected",
    })


def jsonify(data):
    return {
        "text": json.dumps(data),
    }


def reply(message, data):
    message.reply_channel.send(jsonify(data))


def get_player(ppk, round_number):
    players = Player.objects.filter(round_number=round_number, participant__pk=ppk)
    if len(players) == 1:
        return players[0]


def ws_message(message):
    d = dict(message)

    body = json.loads(d['text'])
    round_number = body['round_number']
    action = body['action']
    page = body['page']
    pid = int(body['pid'])

    if action == "report":
        seconds = int(time.time())

        player = get_player(pid, round_number)
        player.update_report_vars(seconds, page)

        #if player.first_to_report:
        #    text = "In this round, you are THE FIRST PLAYER in your group to click on the REPORT button."
        #else:
        #    text = "In this round, you are NOT THE FIRST PLAYER in your group to click on the REPORT button."
        text = "You have reported the use of the chat window."

        reply(message, {
            "text": text,
        })
