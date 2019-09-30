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
    
    # num_rounds is only an upper bound but not actually used
    num_rounds = 30 # TODO: Adjust

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

    def creating_session(self):

        # Apply grouping scheme for each round.
        # Note that this is super game specific
        if self.round_number == 1:
            if self.session.num_participants == 9:
                shuffle_structure = self.this_app_constants()['shuffle_structure_small']
            elif self.session.num_participants == 18:
                shuffle_structure = self.this_app_constants()['shuffle_structure_medium']
            elif self.session.num_participants == 27:
                shuffle_structure = self.this_app_constants()['shuffle_structure_big']
            self.set_group_matrix(shuffle_structure)
        else:
            # For all other rounds in the app, we apply the group structure which we have used for
            # the first round.
            # Hence, the group structure is kept constant within the app.
            # Note however that we change it from super game to super game as we change the 
            # shuffle_structure_***
            self.group_like_round(1)
        
        # treatment assignment
        if self.round_number == 1:
            # Assign the treatment to each group
            # Note that we store it in the *treatment* field in the 
            # first round but also in the participant variables of
            # the first participant in the group to access it across rounds. 
            for g in self.get_groups():
                # *group_treatment* has to be specified in the session config
                treatment_draw = self.session.config['group_treatment']
                
                # Store it in the variable *group_treatment* for first round for the group
                g.group_treatment = treatment_draw

                # Furthermore, store it in the participant variables for the each player in each
                # group to access it accross rounds.
                for p in g.get_players():
                    p.participant.vars['group_treatment'] = treatment_draw

class SharedBaseGroup(BaseGroup):
    class Meta:
        abstract = True

    # Group specific variables for each round in the given SG
    winning_price = models.IntegerField()
    winner_profit = models.IntegerField()
    recommendation = models.IntegerField()
    n_winners = models.IntegerField()

    # Treatment storage
    group_treatment = models.StringField()

    def get_recommendation(self, round_number):
        """ Based on the past round create a new recommendation
        for the following period. 
        This recommendation is based on the following
        simple rule:
        - In the first round recommend the monopoly price
        - In all later round:
            - If all players had the same price in the last period,
              recommend the monopoly price
            - If player played different prices, recommend the deviation
            price
        
        """

        # Get all players for the specific group
        players = self.get_players()

        # If we are not in the first round or if players had the same price in the last period
        #  we recommend the monopoly price
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
        """ A function to set the payoffs for a specific round for a specific 
            group.
        """


        # Get all players for the specific group
        players = self.get_players()

        # Retrieve the winning price for the given round
        self.winning_price = min([p.price for p in players])

        # Get a list of winners in the group, e.g. those who played the winning price
        winners = [p for p in players if p.price == self.winning_price]
        
        # There can be multiple players with the lowest price
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
    # I do not use CurrencyFields since those are weird.
    profit = models.IntegerField()
    accumulated_profit = models.IntegerField()

    is_winner = models.BooleanField()


    # Final payoff is stored again
    final_payoff_euro = models.FloatField()


    def set_final_payoff(self):
        # We take the accumulated payoff from the last round we 
        # played.
        # This is stored as a fake-constant in the subsession, since it is a random draw
        # for each SuperGame and the different supergame apps inherit from this app
        # TODO: Change *round_number_draw* for each super game app.
        last_played_round = self.subsession.this_app_constants()['round_number_draw']

        # Take the accumulated profit from the last round
        # IMPORTANT: Only use this method once the profit for the round has been calculated
        # using *set_profits_round* from the group method
        total_money = self.in_round(last_played_round).accumulated_profit 
        self.payoff = total_money
        # Final points as money
        self.final_payoff_euro = float(self.participant.payoff_plus_participation_fee())

        # Save the final accumulated payoff for the last subgame in the participant dict.
        self.sg_payoff_to_dict(sg_counter = self.subsession.this_app_constants()['super_game_count'],
                               final_payoff = total_money)

    def sg_payoff_to_dict(self, sg_counter, final_payoff):
        """ A helper function to save payoff for each subgame (*final_payoff* for subgame *sg_counter*) to the participant dict.
        """
        key_name = "final_payoff_sg_" + str(sg_counter)        
        self.participant.vars[key_name] = final_payoff

class Subsession(SharedBaseSubsession):
    pass

    def this_app_constants(self):
        """ App specific constants
        
        """
        # The number of rounds we have drawn ex ante according to some cont prob
        return {'round_number_draw': 1, #TODO: Change
                'super_game_count': 1,
                'shuffle_structure_small': [[1,2,3], [4, 5, 6], [7, 8, 9]],
                'shuffle_structure_medium': [[1,2,3], [4, 5, 6], [7, 8, 9],
                                    [10, 11, 12], [13, 14, 15], [16, 17, 18]],
                'shuffle_structure_big': [[1,2,3], [4, 5, 6], [7, 8, 9],
                                    [10, 11, 12], [13, 14, 15], [16, 17, 18],
                                    [19, 20, 21], [22, 23, 24], [25, 26, 27]]
                } 

class Group(SharedBaseGroup):
    pass

class Player(SharedBasePlayer):
    pass


