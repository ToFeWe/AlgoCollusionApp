from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    # Indicator which super game is payed
    payed_sg = models.IntegerField()

    def creating_session(self):
        self.payed_sg = random.choice([1,2,3])

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
