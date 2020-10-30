from django import forms
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from cartelgame.models import Variables, Constants as CartelConstants

from otree.models import Session

author = 'UP Department of Computer Science'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1

    demand_per_round = CartelConstants.demand_per_round
    max_buying_price = CartelConstants.max_buying_price
    players = CartelConstants.players_per_group


class Subsession(BaseSubsession):

    def creating_session(self):
        # Must be called before anything else
        self.setup_treatment()

    def setup_treatment(self):
        if 'treatment' not in self.session.config:
            raise RuntimeError("No treatment specified. Aborting...")
        
    def get_treatment(self):
        return self.session.config['treatment']


class Group(BaseGroup):
    pass


MAXIMUM_PRICE_LABEL = "What is the maximum price that consumers in this experiment are willing to accept?"
MAXIMUM_PRICE_CHOICES = (10, 12, 15)
MAXIMUM_PRICE_FIELD_CHOICES = [(i, i) for i in MAXIMUM_PRICE_CHOICES]

PLAYERS_PER_GROUP_LABEL = "How many players will there be in each group?"
PLAYERS_PER_GROUP_CHOICES = (1, 4, 120)
PLAYERS_PER_GROUP_FIELD_CHOICES = [(i, i) for i in MAXIMUM_PRICE_CHOICES]

CONSUMERS_LABEL = "How many consumers are there in this experiment?"
CONSUMERS_CHOICES = (1, 4, 120)
CONSUMERS_FIELD_CHOICES = [(i, i) for i in MAXIMUM_PRICE_CHOICES]

DISCUSS_CHAT_LABEL = "What can you discuss in the chat window? Tick all that apply."
DISCUSS_CHAT_FIELD_CHOICES = [
    ("offer", "Your offer price"),
    ("personal", "Your personal details"),
    ("location", "Your location in this laboratory"),
]

class Player(BasePlayer):
    pass
