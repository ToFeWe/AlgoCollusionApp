from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1/130,
    participation_fee=4.00,
    doc=""
)

SESSION_CONFIGS = [
    dict(
        name='SELF_treatment_1H1A_players_18',
        display_name="SELF_treatment_1H1A_players_18",
        group_treatment='1H1A',
        num_demo_participants=18,
        expId=1234, #TODO: Change and test once it exists
        expShortName='test',#TODO: Change and test once it exists
        use_browser_bots=False,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'quiz',
         'payment']
    ),
    dict(
        name='SELF_treatment_2H0A_players_18',
        display_name="SELF_treatment_2H0A_players_18",
        group_treatment='2H0A',
        num_demo_participants=18,
        expId=1234,
        expShortName='test',#TODO: Change and test once it exists
        use_browser_bots=False,#TODO: Change and test once it exists
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'quiz',
         'payment']
    ),
    dict(
        name='BOT_treatment_2H0A_players_18',
        display_name="BOT_treatment_2H0A_players_18",
        group_treatment='2H0A',
        num_demo_participants=18,
        expId=1234,
        expShortName='test',
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'quiz',
         'payment']
    ),
    dict(
        name='BOT_treatment_1H1A_players_18',
        display_name="BOT_treatment_1H1A_players_18",
        group_treatment='1H1A',
        num_demo_participants=18,
        expId=1234,
        expShortName='test',
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'quiz',
         'payment']
    ),
    dict(
        name='BOT_treatment_2H1A_players_18',
        display_name="BOT_treatment_2H1A_players_18",
        group_treatment='2H1A',
        num_demo_participants=18,
        expId=1234,
        expShortName='test',
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'quiz',
         'payment']
    ),
    dict(
        name='BOT_treatment_1H2A_players_18',
        display_name="BOT_treatment_1H2A_players_18",
        group_treatment='1H2A',
        num_demo_participants=18,
        expId=1234,
        expShortName='test',
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'quiz',
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
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2

ROOMS = [
    dict(
        name='DICELab',
        display_name='DICELab'
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
