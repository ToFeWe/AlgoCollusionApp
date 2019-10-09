from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01,
    participation_fee=4.00,
    doc=""
)

SESSION_CONFIGS = [
    dict(
        name='bertrand_baseline_test',
        display_name="bertrand_baseline",
        group_treatment='baseline',
        num_demo_participants=9,
        app_sequence=[
         #'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         #'survey',
         'payment'] # TODO: Adjust
    ),
    dict(
        name='test_survey_baseline',
        display_name="test_survey",
        group_treatment='baseline',
        num_demo_participants=9,
        app_sequence=[
         'survey',
         ]
    ),
    dict(
        name='test_survey_recommendation',
        display_name="test_survey_recommendation",
        group_treatment='recommendation',
        num_demo_participants=9,
        app_sequence=[
         'survey',
         ]
    ),
    dict(
        name='test_intro_baseline',
        display_name="test_introduction",
        group_treatment='baseline',
        num_demo_participants=9,
        app_sequence=[
         'introduction',
         ]
    ),
    dict(
        name='test_intro_recommendation',
        display_name="test_introduction_recommendation",
        group_treatment='recommendation',
        num_demo_participants=9,
        app_sequence=[
         'introduction',
         ]
    ),

    dict(
        name='bertrand_recommendation',
        display_name="bertrand_recommendation",
        group_treatment='recommendation',
        num_demo_participants=9,
        app_sequence=['introduction', 'bertrand', 'bertrand_SG_2', 'bertrand_SG_3',  'survey', 'payment']
    ),
    dict(
        name='bertrand_big_recommendation',
        display_name="bertrand_recommendation",
        num_demo_participants=27,
        group_treatment='recommendation',
        app_sequence=['introduction', 'bertrand', 'bertrand_SG_2', 'bertrand_SG_3',  'survey', 'payment']
    )



]
# see the end of this file for the inactive session configs


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
        name='lab101',
        display_name='DICE Lab',
        participant_label_file='_rooms/dice_lab_labels.txt'
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

# inactive session configs
### dict(name='trust', num_demo_participants=2, app_sequence=['trust']),
### dict(name='prisoner', num_demo_participants=2, app_sequence=['prisoner']),
### dict(name='ultimatum', num_demo_participants=2, app_sequence=['ultimatum']),
### dict(name='ultimatum_strategy', num_demo_participants=2, app_sequence=['ultimatum'], use_strategy_method=True),
### dict(name='ultimatum_non_strategy', num_demo_participants=2, app_sequence=['ultimatum'], use_strategy_method=False),
### dict(name='vickrey_auction', num_demo_participants=3, app_sequence=['vickrey_auction']),
### dict(name='volunteer_dilemma', num_demo_participants=3, app_sequence=['volunteer_dilemma']),
### dict(name='cournot', num_demo_participants=2, app_sequence=['cournot']),
### dict(name='principal_agent', num_demo_participants=2, app_sequence=['principal_agent']),
### dict(name='dictator', num_demo_participants=2, app_sequence=['dictator']),
### dict(name='matching_pennies', num_demo_participants=2, app_sequence=['matching_pennies']),
### dict(name='traveler_dilemma', num_demo_participants=2, app_sequence=['traveler_dilemma']),
### dict(name='bargaining', num_demo_participants=2, app_sequence=['bargaining']),
### dict(name='common_value_auction', num_demo_participants=3, app_sequence=['common_value_auction']),
### dict(name='bertrand', num_demo_participants=2, app_sequence=['bertrand']),
### dict(name='real_effort', num_demo_participants=1, app_sequence=['real_effort']),
### dict(name='lemon_market', num_demo_participants=3, app_sequence=['lemon_market']),
### dict(name='public_goods_simple', num_demo_participants=3, app_sequence=['public_goods_simple']),
### dict(name='trust_simple', num_demo_participants=2, app_sequence=['trust_simple']),
