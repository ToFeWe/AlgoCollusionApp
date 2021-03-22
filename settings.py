from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1/110,
    participation_fee=4.00,
    corona_bonus_after_end=4.00,
    doc=""
)

SESSION_CONFIGS = [
    dict(
        name='intro_check',
        display_name="intro_check",
        group_treatment='2H0A',
        num_demo_participants=18,
        use_browser_bots=False,
        app_sequence=[
         'introduction']
    ),
    dict(
        name='SELF_treatment_1H1A_players_18',
        display_name="SELF_treatment_1H1A_players_18",
        group_treatment='1H1A',
        num_demo_participants=18,
        use_browser_bots=False,
        app_sequence=[
        #  'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
        #  'survey',
         'payment']
    ),
    dict(
        name='SELF_treatment_2H0A_players_18',
        display_name="SELF_treatment_2H0A_players_18",
        group_treatment='2H0A',
        num_demo_participants=18,
        use_browser_bots=False,
        app_sequence=[
        #  'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
        #  'survey',
         'payment']
    )



]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
POINTS_CUSTOM_NAME = 'Taler'
USE_POINTS = True
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 1

ROOMS = [
    dict(
        name='test',
        display_name='Test Lab',
        participant_label_file='dicelab_otree_labels.txt'
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = '4e0cd9nd3+-lh=zu1l^vota306m8%2l+#r7vdaph*11nuih33^'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
