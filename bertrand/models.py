from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
Price Recommender Game with Bertrand
"""


class Constants(BaseConstants):
    players_per_group = 3
    name_in_url = 'bertrand'


    # Note that *num_rounds* is used to have an upper bound but is not acutally used
    num_rounds = 100

    # Rounds without continuation probability
    fixed_rounds = 1

    # Probability to continue the experiment for the next round
    cont_prob = 6/7

    instructions_template = 'bertrand/instructions.html'

    maximum_price = 10
    monopoly_price = 10

    # Price that is recommended if there is a deviation from a player
    deviation_price = 1

class Subsession(BaseSubsession):
    def creating_session(self):
        # Variable that shows if we still play
        self.session.vars['playing'] = True

class Group(BaseGroup):
    winning_price = models.IntegerField()
    winner_payoff = models.IntegerField()
    recommendation = models.IntegerField()

    def get_recommendation(self, round_number):
        players = self.get_players()
        # In the first round we always recommend the monopoly price
        if round_number > 1:
            past_recommendation = self.in_previous_rounds()[-1].recommendation
            past_prices = [p.in_previous_rounds()[-1].price for p in players]
            followed_advise = [True if price == past_recommendation else False for price in past_prices]
            if False in followed_advise:
                self.recommendation = Constants.deviation_price
            else:
                self.recommendation = Constants.monopoly_price
        else:
            self.recommendation = Constants.monopoly_price

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
        min=Constants.deviation_price, max=Constants.maximum_price,
        doc="""Price player offers to sell product for"""
    )

    is_winner = models.BooleanField()

    # Quiz Questions
    q_bertrand_1 = models.IntegerField(
        initial=None, 
        label='Stellen Sie sich folgende Situation vor: Sie haben XYZ, die anderen AAA. Wieviel bekommen sie als Profit?'
    )

    q_recommendation_1 = models.StringField(
        initial=None, 
        choices = ['bla', 'blub', 'bli'],
        label='Was ist das Ziel des Empfehlungsalgs?'
    )

    q_recommendation_2 = models.StringField(
        initial=None, 
        choices = ['bla', 'blub', 'bli'],
        label= 'Was denkst du????'
    )

    # Counter variable how often the player has answered smth wrong

    counter_bertrand_1 = models.IntegerField(initial = 0)
    counter_recommendation_1 = models.IntegerField(initial = 0)
    counter_recommendation_2 = models.IntegerField(initial = 0)


    def q_bertrand_1_error_message(self, value):
        if value != 1:
            # Count +1 if the player answered the question wrong
            self.counter_bertrand_1 += 1
            return 'Denken Sie besser noch mal nach'

    def q_recommendation_1error_message(self, value):
        if value != 'bla':
            # Count +1 if the player answered the question wrong
            self.counter_recommendation_1 += 1
            return 'Denken Sie besser noch mal nach'

    def q_recommendation_2_error_message(self, value):
        if value != 'bla':
            # Count +1 if the player answered the question wrong
            self.counter_recommendation_2 += 1
            return 'Denken Sie besser noch mal nach'
