import random
import time

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .globals import NUM_CAUGHT

def is_valid_round(self):
    return self.round_number <= self.subsession.last_round


class WaitToContinuePage(Page):
    
    def is_displayed(self):
        return self.round_number == 1


class WaitForGroupWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass
    
    def is_displayed(self):
        return self.round_number == 1


class WaitForAllWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        pass
    
    def is_displayed(self):
        return self.round_number == 1


class InstructionsPage(Page):
    page_name = "InstructionsPage"

    def is_displayed(self):
        return Constants.part == Constants.ACTUAL and self.round_number == 1


class GroupingInfoPage(Page):
    timeout_seconds = Constants.grouping_info_page_timeout
    
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {self.subsession.get_treatment(): True}


class GroupingWaitPage(WaitPage):

    def after_all_players_arrive(self):
        print("=" * 150)
        print("ROUND", self.round_number, self.subsession.last_round)
        print("=" * 150)

    def is_displayed(self):
        return is_valid_round(self)


class AskForChatPage(Page):
    form_model = 'player'
    form_fields = ['accepted_chat']
    timeout_seconds = 15

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat']

    def accepted_chat_error_message(self, value):
        if value is None:
            return Constants.required_error_message

    def accepted_chat_error_message(self, value):
        if value is None:
            return Constants.required_error_message

    def vars_for_template(self):
        return {
            "seconds_before_flagging": Constants.seconds_before_flagging
        }


class AskForChatWaitPage(WaitPage):

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat']

    def after_all_players_arrive(self):
        self.group.compute_accepted_chat()


class ChatResultsPage(Page):
    timeout_seconds = Constants.chat_results_page_timeout

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat']


class ChatInitWaitPage(WaitPage):

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat']

    def after_all_players_arrive(self):
        if self.group.accepted_chat():
            self.group.set_group_start_time()


class ChatPage(Page):
    timeout_seconds = Constants.chat_duration

    def is_displayed(self):
        return self.group.accepted_chat() and self.player.accepted_chat and is_valid_round(self) and self.session.config['has_chat']

    def before_next_page(self):
        self.player.compute_report()

    def vars_for_template(self):
        return {
            "chat_players": ", ".join(sorted(["Player " + str(p.id_in_group) for p in self.group.get_players() if p.accepted_chat])),
        }


class AfterChatWaitPage(WaitPage):

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat']


# Base page
class PricePage(Page):
    form_model = 'player'
    form_fields = ['agreed_common_price', 'price']
    page_name = "PricePage"

    def price_error_message(self, value):
        if not value:
            return Constants.required_error_message

    def vars_for_template(self):
        price_min = models.Player._meta.get_field('price').min
        price_max = models.Player._meta.get_field('price').max

        return {
            'price_min': price_min,
            'price_max': price_max,
            'page_name': self.page_name,
        }


class PriceForChatPage(PricePage):
    form_model = 'player'
    form_fields = ['agree_count', 'common_price']
    page_name = "PriceForChatPage"

    def is_displayed(self):
        return self.group.accepted_chat() and self.player.accepted_chat and is_valid_round(self) and self.session.config['has_chat']

    def vars_for_template(self):
        return {
            "seconds_before_flagging": Constants.seconds_before_flagging,
            'page_name': self.page_name,
        }

    def error_message(self, values):
        agree_count = values['agree_count']
        common_price = values['common_price']
        if (agree_count != 0 and common_price == None) or (agree_count == 0 and common_price != None):
            return "Agreed-upon price is inconsistent with number of people who agreed."


class OfferPricePage(PricePage):
    form_model = 'player'
    form_fields = ['price']
    page_name = "OfferPricePage"
    timeout_seconds = 60

    def is_displayed(self):
        return is_valid_round(self)

    def vars_for_template(self):
        return {
            "seconds_before_flagging": Constants.offer_timeout,
            'page_name': self.page_name,
        }


class GrossEarningsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.update_units_sold()
        self.group.update_gross_earnings()

    def is_displayed(self):
        return is_valid_round(self)


class GrossEarningsPage(Page):
    timeout_seconds = 45
    page_name = "GrossEarningsPage"

    def is_displayed(self):
        return is_valid_round(self)

    def vars_for_template(self):
        num_caught = NUM_CAUGHT[self.round_number]
        
        return {
            'page_name': self.page_name,
            'num_caught': num_caught,
        }


class DetectionWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.check_for_report()
        self.group.update_penalty()
        self.group.update_additional_penalty()

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat'] and (self.session.config['has_random_detection'] or self.session.config['has_previous_round_detection'])


class PenaltyPage(Page):
    timeout_seconds = Constants.default_timeout

    def is_displayed(self):
        return Constants.part != Constants.PRACTICE and self.session.config['has_random_detection'] and self.group.will_show_penalty_page() and self.player.accepted_chat and is_valid_round(self) and self.session.config['has_chat']


class NoPenaltyPage(Page):
    timeout_seconds = Constants.default_timeout

    def is_displayed(self):
        return Constants.part != Constants.PRACTICE and self.group.accepted_chat() and self.session.config['has_random_detection'] and not self.group.will_be_detected and is_valid_round(self) and self.session.config['has_chat']


class AdditionalPenaltyPage(Page):
    timeout_seconds = Constants.default_timeout

    def is_displayed(self):
        previous_self = self.player.get_previous_self()

        return Constants.part != Constants.PRACTICE and self.group.will_be_sued and self.session.config['has_previous_round_detection'] and previous_self and previous_self.accepted_chat and is_valid_round(self) and self.session.config['has_chat']

    def vars_for_template(self):
        return {
            'previous_round': self.round_number - 1,
        }


class NetEarningsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.update_net_earnings()

    def is_displayed(self):
        return is_valid_round(self)


class NetEarningsPage(Page):
    timeout_seconds = 60
    page_name = "NetEarningsPage"

    def is_displayed(self):
        return is_valid_round(self) and self.session.config['has_chat']

    def before_next_page(self):
        self.player.sync_payoff()

    def vars_for_template(self):
        return {
            'page_name': self.page_name,
        }


class OverallResultsPage(Page):
    timeout_seconds = 60

    def before_next_page(self):
        self.player.sync_payoff()

    def is_displayed(self):
        return Constants.part != Constants.PRACTICE and self.round_number == self.subsession.last_round

    def vars_for_template(self):
        return {
            'total': c(self.player.get_average_earnings() + 100),
        }


class WaitForAllToFinishWaitPage(WaitPage):
    wait_for_all_groups = True
    title_text = "Please read the instructions for the Experimental Session."
    body_text = "Please read the instructions for the Experimental Session."

    def is_displayed(self):
        return Constants.part == Constants.PRACTICE and self.round_number == 5


class WaitForNextPartPage(Page):
    timeout_seconds = 120
    page_name = "WaitForAllWaitPage"

    def is_displayed(self):
        return Constants.part == Constants.PRACTICE and self.round_number == self.subsession.last_round

    def vars_for_template(self):
        return {
            'page_name': self.page_name,
        }


page_sequence = [
    WaitForAllWaitPage,
    InstructionsPage,
    GroupingInfoPage,
    GroupingWaitPage,
    AskForChatPage,
    AskForChatWaitPage,
    ChatResultsPage,
    ChatInitWaitPage,
    AfterChatWaitPage,

    ChatPage,
    OfferPricePage,

    GrossEarningsWaitPage,
    GrossEarningsPage,
    DetectionWaitPage,
    PenaltyPage,
    AdditionalPenaltyPage,
    NetEarningsWaitPage,
    NetEarningsPage,
    OverallResultsPage,
    WaitForAllToFinishWaitPage,
    WaitForNextPartPage,
]
