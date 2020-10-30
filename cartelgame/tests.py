import time

from otree.api import Currency as c, currency_range, Submission, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants


VALID_PRICE_VALUES = ("1", "2", "9", "10", "12")
INVALID_PRICE_VALUES = (
    '-1',
    '0',
    '13',
    '999999',
    '-999999',
    '0.00000000001',
    '12.00000000001',
    '5.4',
    'a5',
    '5a',
    'afsadfsdafsafdlskj;lsfa',
    '#####',
    '.',
)


class RoundTest(object):

    def hook_wrapper(self, hook, bot, *args, **kwargs):
        res = hook(bot, *args, **kwargs)
        if res:
            yield from res
    
    def play(self, bot):
        yield from self.hook_wrapper(self.override_hook, bot)
        yield from self.hook_wrapper(self.start_hook, bot)
        yield from self.hook_wrapper(self.override_round_hook, bot)

        yield from self.hook_wrapper(self.before_initial_price_hook, bot)
        yield from self.hook_wrapper(self.initial_price_hook, bot)
        yield from self.hook_wrapper(self.after_initial_price_hook, bot)

        yield from self.hook_wrapper(self.before_ask_chat_hook, bot)
        yield from self.hook_wrapper(self.ask_chat_decision_hook, bot)
        yield from self.hook_wrapper(self.after_ask_chat_hook, bot)

        yield from self.hook_wrapper(self.before_chat_hook, bot)
        if self.has_cartel_this_round(bot):
            yield from self.hook_wrapper(self.accepted_chat_hook, bot)
        yield from self.hook_wrapper(self.after_chat_hook, bot)

        yield from self.hook_wrapper(self.before_reset_price_hook, bot)
        if self.has_cartel_this_round(bot):
            yield from self.hook_wrapper(self.reset_price_hook, bot)
        yield from self.hook_wrapper(self.after_reset_price_hook, bot)

        if self.is_valid_round(bot):
            yield (pages.RoundResultsPage)

        if self.is_valid_round(bot) and bot.group.will_show_penalty_page():
            yield (pages.PenaltyPage)

        if bot.round_number == bot.subsession.last_round:
            yield (pages.OverallResultsPage)

        yield from self.hook_wrapper(self.end_hook, bot)

    def is_valid_round(self, bot):
        #return bot.round_number <= bot.subsession.last_round
        return bot.round_number <= bot.case

    def start_hook(self, bot):
        pass

    def override_hook(self, bot):
        if bot.player.id_in_group == 1:
            bot.player.override_top_scorer(True)
        else:
            bot.player.override_top_scorer(False)

    def override_round_hook(self, bot):
        # Needed to ensure all "last round" possibilities are tested
        print("OVERRIDING LAST ROUND TO", bot.case)
        bot.subsession.override_last_round(bot.case)

    def before_initial_price_hook(self, bot):
        pass

    def initial_price_hook(self, bot):
        if self.is_valid_round(bot):
            self.test_initial_price_page(bot)
            yield (pages.InitialPricePage, {'initial_price': c(8)})
            self.test_player_initial_price(bot, 8)

    def after_initial_price_hook(self, bot):
        pass

    def before_ask_chat_hook(self, bot):
        pass
    
    def has_cartel_this_round(self, bot):
        return self.is_valid_round(bot)

    def ask_chat_decision_hook(self, bot):
        if self.is_valid_round(bot):
            self.test_ask_for_chat_page(bot)
            yield (pages.AskForChatPage, {'accepted_chat': True})
            self.test_player_accepted_chat(bot)

    def after_ask_chat_hook(self, bot):
        pass

    def before_chat_hook(self, bot):
        pass

    def accepted_chat_hook(self, bot):
        self.test_group_accepted_chat(bot)
        yield (pages.ChatPage)

    def after_chat_hook(self, bot):
        pass

    def before_reset_price_hook(self, bot):
        pass

    def reset_price_hook(self, bot):
        if self.is_valid_round(bot):
            yield (pages.ResetPricePage, {
                'cartel_agree': "True",
                'cartel_price': c(8),
                'reset_price': c(6),
            })
            self.test_player_cartel_price(bot, 8)
            self.test_player_reset_price(bot, 6)

    def after_reset_price_hook(self, bot):
        pass

    def end_hook(self, bot):
        pass

    def test_initial_price_page(self, bot):
        assert 'How much will you sell each unit?' in bot.html

    def test_ask_for_chat_page(self, bot):
        assert 'Do you want to chat with the other people in your group?' in bot.html

    def test_player_accepted_chat(self, bot):
        assert bot.player.accepted_chat == True

    def test_group_accepted_chat(self, bot):
        assert bot.group.accepted_chat == True

    def test_player_rejected_chat(self, bot):
        assert bot.player.accepted_chat == False

    def test_group_rejected_chat(self, bot):
        assert bot.group.accepted_chat == False

    def test_player_initial_price(self, bot, initial_price):
        assert bot.player.initial_price == initial_price

    def test_player_cartel_price(self, bot, cartel_price):
        assert bot.player.cartel_price == cartel_price

    def test_player_reset_price(self, bot, reset_price):
        assert bot.player.reset_price == reset_price


class Round1Test(RoundTest):

    def start_hook(self, bot):
        self.test_info_page(bot)
        yield (pages.InfoPage)

    def test_info_page(self, bot):
        pass
        #assert 'Information' in bot.html


class Round2Test(RoundTest):

    def before_initial_price_hook(self, bot):
        for value in INVALID_PRICE_VALUES:
            self.test_initial_price_page(bot)
            yield SubmissionMustFail(pages.InitialPricePage, {'initial_price': value})

    def before_reset_price_hook(self, bot):
        for value1 in INVALID_PRICE_VALUES:
            for value2 in INVALID_PRICE_VALUES:
                for value3 in ("True", "False"):
                    yield SubmissionMustFail(pages.ResetPricePage, {
                        'cartel_agree': value3,
                        'cartel_price': value1,
                        'reset_price': value2,
                    })

        for value1 in VALID_PRICE_VALUES:
            for value2 in INVALID_PRICE_VALUES:
                for value3 in ("True", "False"):
                    yield SubmissionMustFail(pages.ResetPricePage, {
                        'cartel_agree': value3,
                        'cartel_price': value1,
                        'reset_price': value2,
                    })

        for value1 in INVALID_PRICE_VALUES:
            for value2 in VALID_PRICE_VALUES:
                for value3 in ("True", "False"):
                    yield SubmissionMustFail(pages.ResetPricePage, {
                        'cartel_agree': value3,
                        'cartel_price': value1,
                        'reset_price': value2,
                    })


class Round4Test(RoundTest):

    def has_cartel_this_round(self, bot):
        return False

    def ask_chat_decision_hook(self, bot):
        self.test_ask_for_chat_page(bot)
        yield (pages.AskForChatPage, {'accepted_chat': False})  # All no cartel
        self.test_player_rejected_chat(bot)
        yield (pages.NoChatPage)


class Round5Test(RoundTest):

    def has_cartel_this_round(self, bot):
        return False

    def ask_chat_decision_hook(self, bot):
        self.test_ask_for_chat_page(bot)

        if bot.player.id_in_group == 1:
            yield (pages.AskForChatPage, {'accepted_chat': False})  # All except Player 1 accept cartel
            self.test_player_rejected_chat(bot)
        else:
            yield (pages.AskForChatPage, {'accepted_chat': True})
            self.test_player_accepted_chat(bot)
        yield (pages.NoChatPage)


class Round6Test(RoundTest):
    def has_cartel_this_round(self, bot):
        return False

    def initial_price_hook(self, bot):
        if self.is_valid_round(bot):
            yield (pages.InitialPricePage, {'initial_price': ''})

    def ask_chat_decision_hook(self, bot):
        self.test_ask_for_chat_page(bot)

        # Timeout support hack
        print("Sleeping...")
        time.sleep(Constants.default_timeout * 1.5)
        yield (pages.AskForChatPage)
        self.test_player_accepted_chat(bot)
        yield (pages.NoChatPage)


class Round7Test(RoundTest):

    def initial_price_hook(self, bot):
        if self.is_valid_round(bot):
            yield (pages.InitialPricePage, {'initial_price': ''})

    def reset_price_hook(self, bot):
        if self.is_valid_round(bot):
            # Timeout support hack
            print("Sleeping...")
            time.sleep(Constants.default_timeout * 1.5)
            yield (pages.ResetPricePage)


class PlayerBot(Bot):

    test_round = {}

    cases = Constants.last_round_choices

    def __init__(self, *args, **kwargs):
        super(PlayerBot, self).__init__(*args, **kwargs)

        # Default testing behavior
        normal_round = RoundTest()

        for case in self.cases:
            self.test_round[case] = {}

            for i in range(1, 13):
                self.test_round[case][i] = normal_round

        # All cases must have Round 1 special handling
        for case in self.cases:
            self.test_round[case][1] = Round1Test()

        # Test for invalid form input
        self.test_round[12][2] = Round2Test()

        # Test for 3/3 accept chat
        self.test_round[12][4] = Round4Test()

        # Test for 2/3 accept chat
        self.test_round[12][5] = Round5Test()

        # Test for all blank with no cartel
        #self.test_round[12][6] = Round6Test()

        # Test for all blank with cartel
        #self.test_round[12][7] = Round7Test()

    def play_round(self):
        yield from self.test_round[self.case][self.round_number].play(self)
