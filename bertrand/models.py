from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math
import itertools

doc = """
Price Recommender Game with Bertrand
"""

class Constants(BaseConstants):
    players_per_group = 3
    name_in_url = 'bertrand'
    
    # num_rounds is only an upper bound but not acutally used
    num_rounds = 30 

    maximum_price = 10
    monopoly_price = 10

    # Price that is recommended if there is a deviation from a player
    deviation_price = 1

    # Number of consumers
    m_consumer = 30

    # Treatment names
    treatments = ['baseline', 'recommendation']

class SharedBaseSubsession(BaseSubsession):
    class Meta:
      abstract = True



class SharedBaseGroup(BaseGroup):
    class Meta:
        abstract = True

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

    

class SharedBasePlayer(BasePlayer):
    class Meta:
        abstract = True

    price = models.IntegerField(
        min=Constants.deviation_price, max=Constants.maximum_price,
        doc= """Price player offers to sell product for"""
    )

    # Define all as Integer as they are points/tokens
    # Round specific profit and accumulated profit as points
    profit = models.IntegerField()
    accumulated_profit = models.IntegerField()

    is_winner = models.BooleanField()


    # Final payoff is stored again
    final_payoff_euro = models.FloatField()


    def set_final_payoff(self):
        # We take the accumulated payoff from the last round we 
        # played
        last_played_round = self.subsession.this_app_constants()['round_number_draw']
        total_money = self.in_round(last_played_round).accumulated_profit 
        self.payoff = total_money
        # Final points as money
        self.final_payoff_euro = float(self.participant.payoff_plus_participation_fee())

class Subsession(SharedBaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            if self.session.num_participants == 9:
                shuffle_structure = [[1,2,3], [4, 5, 6], [7, 8, 9]]
            elif self.session.num_participants == 18:
                shuffle_structure = [[1,2,3], [4, 5, 6], [7, 8, 9],
                                    [10, 11, 12], [13, 14, 15], [16, 17, 18]]
            elif self.session.num_participants == 27:
                shuffle_structure = [[1,2,3], [4, 5, 6], [7, 8, 9],
                                    [10, 11, 12], [13, 14, 15], [16, 17, 18],
                                    [19, 20, 21], [22, 23, 24], [25, 26, 27]]
            self.set_group_matrix(shuffle_structure)
        else:
            self.group_like_round(1)

    def this_app_constants(self):
        """ App specific constants
        
        """
        # The number of rounds we have drawn ex ante according to some cont prob
        return {'round_number_draw': 1, #TODO: Change
                'super_game_count': 1
                } 

class Group(SharedBaseGroup):
    pass

class Player(SharedBasePlayer):
    pass


