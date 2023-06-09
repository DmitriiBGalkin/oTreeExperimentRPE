from os import environ

SESSION_CONFIGS = [
     dict(
            name='supergames',
            app_sequence=['CournotSupergame','payment'],
            expShortName="RPE",
            expId=8,
            sessId=55,
            participation_fee=6,
            num_demo_participants=16,
            use_browser_bots=False,
            chat_treatment=False,
            uni_wuppertal=False,
            pre_rolls=True
        ),
]
ROOMS = [
    dict(
        name='econ_lab',
        display_name='Experimental Economics Lab',
        participant_label_file='_rooms/participantLabels.txt',
        use_secure_urls=True
    ),
]
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=6.00, doc=""
)

PARTICIPANT_FIELDS = ["CONTRACT_ORDER"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'
# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False



ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5084339421177'

DEBUG = False
