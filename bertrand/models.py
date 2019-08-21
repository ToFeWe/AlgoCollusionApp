from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math

doc = """
Price Recommender Game with Bertrand
"""

class Constants(BaseConstants):
    players_per_group = 3
    name_in_url = 'bertrand'


    # Note that *num_rounds* is used to have an upper bound but is not actually used
    num_rounds = 100

    # Rounds without continuation probability
    fixed_rounds = 1

    # Probability to continue the experiment for the next round
    cont_prob = 0

    instructions_template = 'bertrand/instructions.html'

    maximum_price = 10
    monopoly_price = 10

    # Price that is recommended if there is a deviation from a player
    deviation_price = 1

    # Number of consumers
    m_consumer = 300


class Subsession(BaseSubsession):
    last_round =  models.IntegerField()
    def creating_session(self):
        # Variable that shows if we still play
        self.session.vars['playing'] = True

class Group(BaseGroup):
    winning_price = models.IntegerField()
    winner_profit = models.IntegerField()
    recommendation = models.IntegerField()
    n_winners = models.IntegerField()

    def get_recommendation(self, round_number):
        """ Based on the past round create a new recommendation
        for the following period. 
        Currently, this recommendation is based on the following
        simple rule:
        - In the first round recommend the monopoly price
        - In all later round:
            - If all players followed the advise in the last round
            rounds, recommend the monopoly price
            - If player played different prices, recommend the deviation
            price
        
        """
        players = self.get_players()

        # If we are not in the first round, we recommend the monopoly price
        # if players had the same price in the last period
        # and else the deviation price
        if round_number > 1:
            past_prices = [p.in_previous_rounds()[-1].price for p in players]
            unique_prices = set(past_prices)
            if len(unique_prices) != 1:
                self.recommendation = Constants.deviation_price
            else:
                self.recommendation = Constants.monopoly_price
        else:
            # In the first round we always recommend the monopoly price
            self.recommendation = Constants.monopoly_price

    def set_profits_round(self):
        players = self.get_players()
        self.winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == self.winning_price]
        self.n_winners = len(winners)
        # Market is shared among all winners
        self.winner_profit = int(self.winning_price * Constants.m_consumer / self.n_winners)

        for p in players:
            if p in winners:
                p.is_winner = True
                p.profit = self.winner_profit
                p.accumulated_profit = sum([p_in_round.profit for p_in_round in p.in_all_rounds()])
            else:
                p.is_winner = False
                p.profit = 0
                p.accumulated_profit = sum([p_in_round.profit for p_in_round in p.in_all_rounds()])

    

class Player(BasePlayer):
    price = models.IntegerField(
        min=Constants.deviation_price, max=Constants.maximum_price,
        doc="""Price player offers to sell product for"""
    )

    # Define all as Integer as they are points/tokens

    # Round specific profit and accumulated profit as points
    profit = models.IntegerField()
    accumulated_profit = models.IntegerField()

    is_winner = models.BooleanField()


    # Final payoff is stored again
    final_payoff_euro = models.FloatField()


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

    def q_recommendation_1_error_message(self, value):
        if value != 'bla':
            # Count +1 if the player answered the question wrong
            self.counter_recommendation_1 += 1
            return 'Denken Sie besser noch mal nach'

    def q_recommendation_2_error_message(self, value):
        if value != 'bla':
            # Count +1 if the player answered the question wrong
            self.counter_recommendation_2 += 1
            return 'Denken Sie besser noch mal nach'


    def set_final_payoff(self):
        # We take the accumulated payoff from the last round we 
        # actually played
        last_played_round = self.session.vars['last_round']
        total_money = self.in_round(last_played_round).accumulated_profit 
        self.payoff = total_money
        # Final points as money
        self.final_payoff_euro = c(self.payoff).to_real_world_currency(self.session)