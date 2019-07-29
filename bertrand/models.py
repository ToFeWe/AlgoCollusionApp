from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
2 firms complete in a market by setting prices for homogenous goods.

See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    players_per_group = 3
    name_in_url = 'bertrand'
    num_rounds = 3

    cont_prob = 6/7
    instructions_template = 'bertrand/instructions.html'

    maximum_price = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    winning_price = models.IntegerField()
    winner_payoff = models.IntegerField()

    def set_payoffs_round(self):
        players = self.get_players()
        self.winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == self.winning_price]
        winner_payoff = self.winning_price / len(winners)

        for p in players:
            if p in winners:
                p.is_winner = True
                p.payoff = winner_payoff
            else:
                p.is_winner = False
                p.payoff = 0

    

class Player(BasePlayer):
    price = models.IntegerField(
        min=0, max=Constants.maximum_price,
        doc="""Price player offers to sell product for"""
    )

    is_winner = models.BooleanField()
