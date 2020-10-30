import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = '!x$ta9x$s)xy!uhfu+cqt839y--ru-(rv$jk+kf4l$=9g5+v-4'

# DATABASES = {
#     'default': dj_database_url.config(
#         # Rather than hardcoding the DB parameters here,
#         # it's recommended to set the DATABASE_URL environment variable.
#         # This will allow you to use SQLite locally, and postgres/mysql
#         # on the server
#         # Examples:
#         # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
#         # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

#         # fall back to SQLite if the DATABASE_URL env var is missing
#         default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
#     )
# }

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'Php'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_HTML = """
oTree games
"""

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    # to use qualification requirements, you need to uncomment the 'qualification' import
    # at the top of this file.
    'qualification_requirements': [],
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.000,
    'participation_fee': 100.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

APP_SEQUENCE = ['cartelgame']
APP_SEQUENCE_PRACTICE = ['cartelpractice']
NUM_DEMO_PARTICIPANTS = 4

SESSION_CONFIGS = [
    {
        'name': 'pcc_practice',
        'display_name': 'Cartel Game - Practice',
        'num_demo_participants': NUM_DEMO_PARTICIPANTS,
        'app_sequence': APP_SEQUENCE_PRACTICE,
        'treatment': 'practice',

        'report_action': "Report",
        'has_chat': True,
        'self_report': False,
        'has_random_detection': False,
        'has_previous_round_detection': False,
        'has_announcement': False,
        'reduced_chat_penalty_percentage': 0,
        'chat_penalty_percentage': 0,
        'chat_detection_chance': 0,
        'criminal_case_chance': 0,
    },
    {
        'name': 'pcc_no_aa',
        'display_name': 'Cartel Game - No AA',
        'num_demo_participants': NUM_DEMO_PARTICIPANTS,
        'app_sequence': APP_SEQUENCE,
        'treatment': 'no_aa',

        'report_action': "Report",
        'has_chat': True,
        'self_report': False,
        'has_random_detection': False,
        'has_previous_round_detection': False,
        'has_announcement': False,
        'reduced_chat_penalty_percentage': 0,
        'chat_penalty_percentage': 0,
        'chat_detection_chance': 0,
        'criminal_case_chance': 0,
    },
    {
        'name': 'pcc_with_aa',
        'display_name': 'Cartel Game - With AA',
        'num_demo_participants': NUM_DEMO_PARTICIPANTS,
        'app_sequence': APP_SEQUENCE,
        'treatment': 'with_aa',

        'report_action': "Report",
        'has_chat': True,
        'self_report': False,
        'has_random_detection': True,
        'has_previous_round_detection': False,
        'has_announcement': False,
        'reduced_chat_penalty_percentage': 100,
        'chat_penalty_percentage': 100,
        'chat_detection_chance': 15,
        'criminal_case_chance': 0,
    },
    {
        'name': 'pcc_aa_leniency',
        'display_name': 'Cartel Game - AA with Leniency',
        'num_demo_participants': NUM_DEMO_PARTICIPANTS,
        'app_sequence': APP_SEQUENCE,
        'treatment': 'aa_leniency',

        'report_action': "Report",
        'has_chat': True,
        'self_report': True,
        'has_random_detection': True,
        'has_previous_round_detection': False,
        'has_announcement': False,
        'reduced_chat_penalty_percentage': 100,
        'chat_penalty_percentage': 100,
        'chat_detection_chance': 15,
        'criminal_case_chance': 0,
    },
    {
        'name': 'pcc_aa_no_leniency_reputation',
        'display_name': 'Cartel Game - AA without Leniency and with Reputation',
        'num_demo_participants': NUM_DEMO_PARTICIPANTS,
        'app_sequence': APP_SEQUENCE,
        'treatment': 'aa_no_leniency_reputation',

        'report_action': "Report",
        'has_chat': True,
        'self_report': False,
        'has_random_detection': True,
        'has_previous_round_detection': False,
        'has_announcement': True,
        'reduced_chat_penalty_percentage': 100,
        'chat_penalty_percentage': 100,
        'chat_detection_chance': 15,
        'criminal_case_chance': 0,
    },
    {
        'name': 'pcc_aa_leniency_reputation',
        'display_name': 'Cartel Game - AA with Leniency and Reputation',
        'num_demo_participants': NUM_DEMO_PARTICIPANTS,
        'app_sequence': APP_SEQUENCE,
        'treatment': 'aa_leniency_reputation',

        'report_action': "Report",
        'has_chat': True,
        'self_report': True,
        'has_random_detection': True,
        'has_previous_round_detection': False,
        'has_announcement': True,
        'reduced_chat_penalty_percentage': 100,
        'chat_penalty_percentage': 100,
        'chat_detection_chance': 15,
        'criminal_case_chance': 0,
    },
]

CHANNEL_ROUTING = 'routing.channel_routing'

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())

ROOM_DEFAULTS = {}

ROOMS = [
    {
        'name': 'sessionq',
        'display_name': 'Session Q',
        'participant_label_file': 'labels.txt',
    },
    {
        'name': 'sessionr',
        'display_name': 'Session R',
        'participant_label_file': 'labels.txt',
    },
]

DEBUG = 1
