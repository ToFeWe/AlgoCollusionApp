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
        name='BOT_recommendation_full_27',
        display_name="BOT_recommendation_full_27",
        group_treatment='recommendation',
        num_demo_participants=27,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment'] # TODO: Adjust
    ),
    dict(
        name='BOT_recommendation_full_9',
        display_name="BOT_recommendation_full_9",
        group_treatment='recommendation',
        num_demo_participants=9,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment'] # TODO: Adjust
    ),
    dict(
        name='SELF_recommendation_full_9',
        display_name="SELF_recommendation_full_9",
        group_treatment='recommendation',
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
        name='SELF_baseline_full_9',
        display_name="SELF_baseline_full_9",
        group_treatment='baseline',
        num_demo_participants=9,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
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
