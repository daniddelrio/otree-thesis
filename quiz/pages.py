from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class FirstWaitPage(WaitPage):
   title_text = "Instructions"
   body_text = "Welcome to this experiment on decision-making. Please remain quietly seated while you wait for instructions."

class QuizPage(Page):

    def vars_for_template(self):
        return {
            self.subsession.get_treatment(): True,
            "continue_message": "Please wait for the experiment to continue.",
            "right_message": "Your answer is correct.",
            "wrong_message": "Your answer is incorrect.",
            "not_all_right_message": "Incorrect. Please refer to the printed instructions.",
            "still_wrong_message": "Incorrect. Please raise your hand and an experimenter will assist you.",
        }


page_sequence = [
    FirstWaitPage,
    QuizPage,
]
