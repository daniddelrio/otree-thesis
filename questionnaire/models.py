from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


GENDER_FIELD_CHOICES = [
    (1, "Male"),
    (2, "Female"),
]

EDUCATION_LEVEL_FIELD_CHOICES = [
    (1, "Undergraduate"),
    (2, "Graduate school"),
    (3, "Law school"),
    (4, "Other"),
]

WORK_HOURS_FIELD_CHOICES = [
    (1, "Less than 20 hours"),
    (2, "20 to 30 hours"),
    (3, "More than 30 hours"),
]

BETTING_TIMES_FIELD_CHOICES = [
    (1, "Once"),
    (2, "2 to 5 times"),
    (3, "6 to 10 times"),
    (4, "More than 10 times"),
]

Y_N_FIELD_CHOICES = [
    (True, "Yes"),
    (False, "No"),
]

AGREEMENT_FIELD_CHOICES = [
    (1, "Strongly disagree"),
    (2, "Disagree"),
    (3, "Agree"),
    (4, "Strongly agree"),
]

SCALE_CHOICES = [
    (1, "1 (lowest)"),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, "5 (highest)"),
]


class Player(BasePlayer):
    gender = models.IntegerField(label="You consider yourself as:", choices=GENDER_FIELD_CHOICES)
    birthyear = models.IntegerField(label="Your year of birth:", min=1917, max=2004)
    country = models.LongStringField(label="Country where you grew up in:", max_length=100)
    education_level = models.IntegerField(label="What level of education are you currently pursuing?", choices=EDUCATION_LEVEL_FIELD_CHOICES)
    degree_program = models.LongStringField(label="What degree program are you currently pursuing?", max_length=100)

    organizations = models.LongStringField(label="Are you a member of the following organizations? Tick all that apply to you.", max_length=100)

    employed = models.BooleanField(label="Are you currently employed?", widget=widgets.RadioSelect)
    work_hours = models.IntegerField(label="How many hours do you normally work in a week?", null=True, blank=True, choices=WORK_HOURS_FIELD_CHOICES)

    selling_goods = models.BooleanField(label="Do you have any experience in selling goods?", widget=widgets.RadioSelect)
    sold_goods = models.LongStringField(label="What did you sell?", max_length=100, null=True, blank=True)

    consumer_benefit_cartel = models.BooleanField(label="In your opinion, will consumers benefit if sellers of the same or similar goods discuss their offer price?", choices=Y_N_FIELD_CHOICES, widget=widgets.RadioSelect)
    first_thing_cartel = models.LongStringField(label="What is the first thing that comes to mind when you hear the word \"cartel\"?", max_length=100, null=True, blank=True)

    betting = models.BooleanField(label="Did you engage in any better of gambling activity (e.g., lottery, bingo, poker, card games, horse racing, etc.) in the past 6 months?", widget=widgets.RadioSelect)
    betting_times = models.IntegerField(label="How many times did you engage in at least one of these activities in the past 6 months?", null=True, blank=True, choices=BETTING_TIMES_FIELD_CHOICES)

    violate_convenient = models.IntegerField(label="I am willing to violate a rule if it is convenient for me.", choices=AGREEMENT_FIELD_CHOICES)
    violate_unlikely_caught = models.IntegerField(label="I will violate a rule if it is unlikely that I will be caught.", choices=AGREEMENT_FIELD_CHOICES)
    violate_like = models.IntegerField(label="I like violating rules.", choices=AGREEMENT_FIELD_CHOICES)
    violate_harm = models.IntegerField(label="It is alright to violate a rule if it does not harm anyone.", choices=AGREEMENT_FIELD_CHOICES)

    risk_fun = models.IntegerField(label="The greater the risk, the more fun the activity.", choices=SCALE_CHOICES)
    new_situation = models.IntegerField(label="I like the feeling that comes from entering a new situation.", choices=SCALE_CHOICES)
    immoral = models.IntegerField(label="I do not let the fact that something is considered immoral to stop me from doing it.", choices=SCALE_CHOICES)
    illegal = models.IntegerField(label="I do not let the fact that something is illegal to stop me from doing it.", choices=SCALE_CHOICES)
    society = models.IntegerField(label="I often think about doing things that I know society would disapprove of", choices=SCALE_CHOICES)
