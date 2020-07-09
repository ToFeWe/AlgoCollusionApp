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
        name='BOT_recommendation_simple_full_27',
        display_name="BOT_recommendation_simple_full_27",
        group_treatment='recommendation_simple',
        num_demo_participants=27,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='BOT_baseline_full_27',
        display_name="BOT_baseline_full_27",
        group_treatment='baseline',
        num_demo_participants=27,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='BOT_recommendation_lowest_price_full_27',
        display_name="BOT_recommendation_lowest_price_full_27",
        group_treatment='recommendation_lowest_price',
        num_demo_participants=27,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='BOT_recommendation_static_full_27',
        display_name="BOT_recommendation_static_full_27",
        group_treatment='recommendation_static',
        num_demo_participants=27,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='BOT_recommendation_theory_full_27',
        display_name="BOT_recommendation_theory_full_27",
        group_treatment='recommendation_theory',
        num_demo_participants=27,
        use_browser_bots=True,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='SELF_recommendation_simple_full_27',
        display_name="SELF_recommendation_simple_full_27",
        group_treatment='recommendation_simple',
        num_demo_participants=27,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='SELF_baseline_full_27',
        display_name="SELF_baseline_full_27",
        group_treatment='baseline',
        num_demo_participants=27,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='SELF_recommendation_lowest_price_full_27',
        display_name="SELF_recommendation_lowest_price_full_27",
        group_treatment='recommendation_lowest_price',
        num_demo_participants=27,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='SELF_recommendation_static_full_27',
        display_name="SELF_recommendation_static_full_27",
        group_treatment='recommendation_static',
        num_demo_participants=27,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
         'payment']
    ),
    dict(
        name='SELF_recommendation_theory_full_27',
        display_name="SELF_recommendation_theory_full_27",
        group_treatment='recommendation_theory',
        num_demo_participants=27,
        app_sequence=[
         'introduction',
         'bertrand',
         'bertrand_SG_2', 
         'bertrand_SG_3', 
         'survey',
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
        name='dice_lab',
        display_name='DICE Lab',
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
