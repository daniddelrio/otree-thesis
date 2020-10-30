from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class QuestionnairePage(Page):
    form_model = 'player'
    form_fields = [
        "gender",
        "birthyear",
        "country",
        "education_level",
        "degree_program",
        "employed",
        "work_hours",
        "selling_goods",
        "sold_goods",
        "consumer_benefit_cartel",
        "betting",
        "betting_times",
        "violate_convenient",
        "violate_unlikely_caught",
        "violate_like",
        "violate_harm",
        "risk_fun",
        "new_situation",
        "immoral",
        "illegal",
        "society",
    ]

    def vars_for_template(self):
        return {
            "earnings": self.participant.payoff_plus_participation_fee(),
            "invalid_year": "Please enter a valid year.",
            "blank_answer": "Please input your answer.",
            "field_groups": [
                ("gender",),
                ("birthyear",),
                ("country",),
                ("education_level", "degree_program"),
                ("employed",),
                ("work_hours",),
                ("selling_goods",),
                ("sold_goods",),
                ("consumer_benefit_cartel",),
                ("betting",),
                ("betting_times",),
                ("violate_convenient", "violate_unlikely_caught", "violate_like", "violate_harm"),
                ("risk_fun", "new_situation", "immoral", "illegal", "society"),
            ],
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class EndPage(Page):
    pass


page_sequence = [
    QuestionnairePage,
    ResultsWaitPage,
    EndPage,
]
