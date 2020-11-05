import math
import time
import random
from collections import namedtuple

from django import forms
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.forms import Slider
from otree.models import Session

from .locals import *


author = 'UP Department of Computer Science'

doc = """
PCC Cartel Game
"""


class Constants(BaseConstants):
    name_in_url = NAME_IN_CARTEL
    players_per_group = 4
    num_rounds = NUM_ROUNDS

    part = PART
    PRACTICE = PRACTICE
    ACTUAL = ACTUAL

    per_player_supply = 50
    demand_per_round = 120
    #last_round_choices = (5,)
    last_round_choices = (8, 9, 10, 11, 12)

    min_selling_price = 1
    max_selling_price = 12
    max_buying_price = 12

    minimum_players_for_chat = 2

    default_timeout = 10
    chat_duration = 60
    grouping_info_page_timeout = 10
    chat_results_page_timeout = 10
    seconds_before_flagging = 10
    offer_timeout = 30

    required_error_message = "Please input your answer for this item."


LAST_ROUND_FIELD_CHOICES = [(i, i) for i in Constants.last_round_choices]


# Used for accessing pseudoconstants attribute-style in Session
class Variables(object):
    pass


class Subsession(BaseSubsession):
    last_round = models.IntegerField(choices=LAST_ROUND_FIELD_CHOICES)
    treatment = models.StringField(max_length=20)

    def creating_session(self):
        # Subsession.creating_session is called at the start; once for each round
        if self.round_number == 1:
            self.setup_once()

        self.setup_for_each_round()
        self.setup_groups()

    def get_treatment(self):
        return self.session.config['treatment']

    # Single instantiation
    def setup_once(self):
        self.session.vars['last_round'] = random.choice(Constants.last_round_choices)
        self.session.vars['game_start_time'] = time.time()

    def setup_for_each_round(self):
        self.last_round = self.session.vars['last_round']
        
    def setup_groups(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)
        self.setup_penalties()

    def setup_penalties(self):
        groups = self.get_groups() 

        if self.session.config['has_random_detection']:
            for group in groups:
                chance = random.randint(1, 100)
                group.will_be_detected = chance <= self.session.config['chat_detection_chance']
        else:
            for group in groups:
                group.will_be_detected = False

        # Round 1 has no previous round
        if self.session.config['has_previous_round_detection'] and self.round_number != 1:
            for group in groups:
                chance = random.randint(1, 100)
                group.will_be_sued = chance <= self.session.config['criminal_case_chance']
        else:
            for group in groups:
                group.will_be_sued = False

    def get_previous_subsession(self):
        return self.in_round(self.round_number - 1) if self.round_number != 1 else None

    def get_treatment(self):
        return self.session.config['treatment']
    
    def vars_for_admin_report(self):
        players = self.get_players()
        max_payoff = max([p.payoff for p in players])
        return dict(players=players, max_payoff=max_payoff)


class Group(BaseGroup):
    accepted_chat_count = models.IntegerField()
    is_reported = models.BooleanField()
    will_be_detected = models.BooleanField()
    will_be_sued = models.BooleanField()
    reputation_num = models.IntegerField()

    def accepted_chat(self):
        return self.accepted_chat_count >= Constants.minimum_players_per_chat

    def get_reputation_num(self):
        if self.session.config['has_announcement']:
            self.reputation_num = NUM_CAUGHT[self.round_number]

    def get_previous_group(self):
        return self.in_round(self.round_number - 1) if self.round_number != 1 else None

    def will_show_penalty_page(self):
        return Constants.part != Constants.PRACTICE and self.accepted_chat() and (self.will_be_detected or self.is_reported)

    def will_show_additional_penalty_page(self):
        if self.round_number == 1:
            return False

        return Constants.part != Constants.PRACTICE and self.get_previous_group().accepted_chat and self.will_be_sued

    def check_for_report(self):
        players = self.get_players()
        has_report = any(player.reported for player in players)

        if has_report:
            # Get fastest reporter
            sorted_players = sorted(players, key=lambda p: (1 if p.reported else 2, p.report_time))
            sorted_players[0].first_to_report = True

            for player in sorted_players[1:]:
                player.first_to_report = False

        self.is_reported = has_report

        return has_report

    def update_units_sold(self):
        valid_sellers = []

        for player in self.get_players():
            # price can be None
            if player.price and Constants.min_selling_price <= player.price <= Constants.max_buying_price:
                valid_sellers.append(player)

        """
        Algorithm:
        * Sort sellers in buckets based on selling price
        * For each bucket starting from the smallest:
          * If bucket has only one seller:
            * Reduce demand with seller supply
          * Else:
            * Reduce demand by proportionality rule
        """

        # Returns (sold, remaining_demand)
        def sell(supply, remaining_demand):
            sold = 0

            if remaining_demand < supply:
                sold = remaining_demand
                remaining_demand = 0
            else:
                sold = supply
                remaining_demand -= supply

            return (sold, remaining_demand)

        demand = Constants.demand_per_round
        buckets = {price: [] for price in (player.price for player in valid_sellers)}
        for player in valid_sellers:
            buckets[player.price].append(player)

        for price in sorted(buckets):
            bucket = buckets[price]

            if len(bucket) == 1:
                player = bucket[0]
                player.units_sold, demand = sell(player.get_supply(), demand)
            else:
                demand_split = math.floor(demand / len(bucket))

                for player in bucket:
                    player.units_sold, excess = sell(player.get_supply(), demand_split)
                    demand -= demand_split
                    demand += excess

    def update_gross_earnings(self):
        for player in self.get_players():
            player.update_gross_earnings()

    def update_penalty(self):
        for player in self.get_players():
            player.update_penalty()

    def update_additional_penalty(self):
        for player in self.get_players():
            player.update_additional_penalty()

    def update_net_earnings(self):
        for player in self.get_players():
            player.update_net_earnings()

    def set_group_start_time(self):
        start_time = time.time()

        for player in self.get_players():
            # Will be the same for all players who accepted
            if player.accepted_chat:
                player.participant.vars['chat_start_time'] = start_time

    def compute_accepted_chat(self):
        self.accepted_chat_count = sum(player.accepted_chat for player in self.get_players())

    def accepted_chat(self):
        return self.accepted_chat_count and self.accepted_chat_count >= Constants.minimum_players_for_chat


PRICE_FIELD_CHOICES = [(i, i) for i in range(Constants.min_selling_price, Constants.max_selling_price + 1)]

AGREE_COUNT_LABEL = "How many players in your group agreed on a common offer price in this round?"
AGREE_COUNT_CHOICES = [
    (4, "All 4"),
    (3, "Only 3"),
    (2, "Only 2"),
    (0, "No one"),
]

COMMON_PRICE_LABEL = "What price did you agree on?" 
"""
COMMON_PRICE_CHOICES = [
    ("", "No agreed-upon price"),
] + PRICE_FIELD_CHOICES
"""
COMMON_PRICE_CHOICES = PRICE_FIELD_CHOICES

# Per round instance
class Player(BasePlayer):
    units_sold = models.IntegerField(default=0)
    gross_earnings = models.CurrencyField(default=0)
    penalty = models.CurrencyField(default=0)
    additional_penalty = models.CurrencyField(default=0)
    net_earnings = models.CurrencyField(default=0)

    accepted_chat = models.BooleanField(default=None)
    agree_count = models.IntegerField(label=AGREE_COUNT_LABEL, choices=AGREE_COUNT_CHOICES)
    common_price = models.IntegerField(blank=True, label=COMMON_PRICE_LABEL, choices=COMMON_PRICE_CHOICES)

    price = models.IntegerField(default=None, choices=PRICE_FIELD_CHOICES, min=Constants.min_selling_price, max=Constants.max_selling_price)

    reported = models.BooleanField(blank=True, default=None)
    report_time = models.IntegerField(blank=True, default=None)
    report_page = models.StringField(blank=True, default=None, max_length=30)
    first_to_report = models.BooleanField(blank=True, default=None)

    def live_report(self, data):

        # d = dict(data)

        # body = json.loads(d['text'])
        body = data
        round_number = body['round_number']
        action = body['action']
        page = body['page']
        pid = int(body['pid'])
        print(data)
        if action == "report":
            seconds = int(time.time())

            self.update_report_vars(seconds, page)

            #if player.first_to_report:
            #    text = "In this round, you are THE FIRST PLAYER in your group to click on the REPORT button."
            #else:
            #    text = "In this round, you are NOT THE FIRST PLAYER in your group to click on the REPORT button."
            text = "You have reported the use of the chat window."

            # reply(message, {
            #     "text": text,
            # })

            print("Received a report", data)
            return {self.id_in_group: {"text" : text, }}

    def get_previous_self(self):
        return self.in_round(self.round_number - 1) if self.round_number != 1 else None

    def update_gross_earnings(self):
        self.gross_earnings = self.units_sold * self.price

    def update_penalty(self):
        if self.group.will_show_penalty_page() and self.accepted_chat:
            penalty = self.gross_earnings * self.session.config['chat_penalty_percentage'] / 100.0

            if self.first_to_report:
                penalty *= (100 - self.session.config['reduced_chat_penalty_percentage']) / 100.0

            self.penalty = penalty

    def update_additional_penalty(self):
        old = self.get_previous_self()

        if self.group.will_show_additional_penalty_page() and old and old.accepted_chat:
           self.additional_penalty = old.gross_earnings * self.session.config['chat_penalty_percentage'] / 100.0

    def update_net_earnings(self):
        self.net_earnings = self.gross_earnings - self.penalty - self.additional_penalty

    def compute_report(self):
        if self.reported is None:
            self.reported = False
        elif self.reported and 'chat_start_time' in self.participant.vars:
            self.report_time = int(time.time() - self.participant.vars['chat_start_time'])

    def get_supply(self):
        return Constants.per_player_supply

    def update_report_vars(self, seconds, page):
        self.report_time = seconds
        self.reported = True
        self.report_page = page
        self.first_to_report = self.compute_first_to_report()
        self.save()

    def compute_first_to_report(self):
        if not self.report_time:
            return False

        for peer in self.get_others_in_group():
            if peer.report_time and peer.report_time < self.report_time:
                return False

        return True

    def get_net_earnings_per_round(self):
        return [p.net_earnings for p in self.in_all_rounds()]

    def get_total_earnings(self):
        return sum(self.get_net_earnings_per_round())

    def get_average_earnings_per_round(self):
        return self.get_total_earnings() / self.round_number

    def sync_payoff(self):
        average = self.get_average_earnings_per_round()
        self.payoff = average