from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy as np
import math
doc = """
An Experiment on Algorithmic Collusion.
"""

class Constants(BaseConstants):
    players_per_group = None
    name_in_url = 'algcoll'
    
    # num_rounds is only an upper bound but not actually used
    num_rounds = 30 

    maximum_price = 6
    reservation_price = 5
    stage_game_NE = 1
    lowest_price = 0 

    
    # Number of consumers
    m_consumer = 60

    # Treatment names
    treatments = ['3H0A', '2H0A', '2H1A', '1H2A', '1H1A']

    firma_id_map = {1: 'A',
                    2: 'B',
                    3: 'C'}
    


class SharedBaseSubsession(BaseSubsession):
    class Meta:
      abstract = True

    def creating_session(self):

        # Apply grouping scheme for each round.
        # Note that this is super game and treatment specific.
        if self.round_number == 1:
            
            # Check for the given treatment, how large our matching group
            # has to be.
            if self.session.config['group_treatment'] == '3H0A':
                group_size = 3
            elif self.session.config['group_treatment'] in ['2H0A', '2H1A']:
                group_size = 2
            else:
                group_size = 1
            
            # Get the group matching for the current super game
            n_participants = self.session.num_participants
            if group_size == 3:
                if n_participants not in [9, 18]:
                    raise Exception(("In the 3H0A treatment we need matching groups of 9 people.",
                                     "The Maximum number of subjects is 18.",                                    
                                     "One of the conditions is not met given {} participants.".format(n_participants)))
                else:
                    if n_participants == 9:
                        shuffle_structure = self.this_app_constants()['group_shuffle_by_size'][group_size]['shuffle_structure_small']
                    elif n_participants == 18:
                        shuffle_structure = self.this_app_constants()['group_shuffle_by_size'][group_size]['shuffle_structure_medium']
            elif group_size == 2:
                if n_participants not in [6, 12, 18]:
                    raise Exception(("In the 3H0A treatment we need matching groups of 6 people.",
                                     "The Maximum number of subjects is 18.",                                    
                                     "One of the conditions is not met given {} participants.".format(n_participants)))
                else:
                    if n_participants == 6:
                        shuffle_structure = self.this_app_constants()['group_shuffle_by_size'][group_size]['shuffle_structure_small']
                    elif n_participants == 12:
                        shuffle_structure = self.this_app_constants()['group_shuffle_by_size'][group_size]['shuffle_structure_medium']
                    elif n_participants == 18:
                        shuffle_structure = self.this_app_constants()['group_shuffle_by_size'][group_size]['shuffle_structure_big']
            else:
                # In the individual choice treatments, we do not have a group matching
                # but everyone is in his/her own group.
                # This is still needed as we use the group class for all market information.
                shuffle_structure = [[i] for i in range(1, self.session.num_participants + 1)]

            print(shuffle_structure)
            self.set_group_matrix(shuffle_structure)
        else:
            # For all other rounds in the app, we apply the group structure which we have used for
            # the first round.
            # Hence, the group structure is kept constant within the app.
            # Note however that we change it from super game to super game as we change the 
            # shuffle_structure_***
            self.group_like_round(1)
        
        # Assign the treatment to each player in the session
        # Note that we store it in the *treatment* field in the 
        # all rounds but also in the participant variables of
        # the first participant in the group to access it across rounds. 
        for g in self.get_groups():
            # *group_treatment* has to be specified in the session config
            # Store it in the variable *group_treatment* for first round for the group
            g.group_treatment = self.session.config['group_treatment']

            # Also store it for each participant
            if self.round_number == 1:
                for p in g.get_players():
                    # Furthermore, store it in the participant variables for the each player in each
                    # group to access it accross rounds.
                    p.participant.vars['group_treatment'] = self.session.config['group_treatment']
                    
                    # Init payoff variable for dict to zero at the start of the game
                    # to avoid errors on the admin page.
                    # Will be adjusted over the course of the game.
                    sg_counter = self.this_app_constants()['super_game_count']
                    key_name = "final_payoff_sg_" + str(sg_counter)        
                    p.participant.vars[key_name] = 0
    
    def vars_for_admin_report(self):
        all_groups = self.get_groups()
        return {
            'all_groups': all_groups
        }

class SharedBaseGroup(BaseGroup):
    class Meta:
        abstract = True    

    # We use the group as a market level
    # Hence, also in the "individual" choice treatments
    # e.g. the treatments with only one human and algorithms
    # those variables are used to store outcomes.
    winning_price = models.IntegerField()
    winner_profit = models.IntegerField()
    n_winners = models.IntegerField()

    # Prices of the algorithm(s)
    # Note that in markets with two algorithms,
    # the price of those algorithms must be
    # symmetric, given its the same with the same input.
    price_algorithm = models.IntegerField()
    profit_algorithm = models.FloatField()
    accumulated_profit_algorithm = models.FloatField()

    # Treatment storage
    group_treatment = models.StringField()

    def set_algo_price(self):
        """
        
        A function to get the price of the algorithmic player
        in the given round given the prices that haven been played
        in the last round.
        Also calculates the profit of the algorithmic seller.

        TODO: Do I want a delay for the algorithm to get its price?
        Else, in comparison to humans, it is much faster in a treatment
        with algorithms.
        TODO: I should somehow define a data structure that saves the decisions
        of the algorithms in a more structured level on the group level
        to be able to save it for the pay out of the players who "use"
        the algorithm
        """
        treatment = self.group_treatment
        
        # Price for the algorithm is only needed if
        # there is actually an algorithm at play!
        if treatment not in ['3H0A', '2H0A']:
            # We have an initial condition problem here
            # Assumption will be that the state in the 
            # hypothetical state 0 is the state of convergence
            # from the simulation study.
            if self.round_number == 1:
                # TODO: Adjust for state of convergence
                if treatment == '1H1A':
                    past_prices_tuple = (Constants.reservation_price, Constants.reservation_price)
                else:
                    past_prices_tuple = (Constants.reservation_price, Constants.reservation_price,
                                        Constants.reservation_price)
            # In later round we can look back on the history of the game
            # and use this information to get the current prices for the algorithm
            else:
                past_algo_price = [self.in_previous_rounds()[-1].price_algorithm]
                all_past_human_prices = [p.in_previous_rounds()[-1].price for p in self.get_players()]
                
                if treatment == '1H2A':
                    past_prices_tuple = tuple(past_algo_price + past_algo_price + all_past_human_prices)
                else:
                    past_prices_tuple = tuple(past_algo_price + all_past_human_prices)
            
            # TODO: Import algorithms and save to Constants
            # # differ which algorithm to use by treatment (3 or 2 firm market)
            # if treatment in ['1H2A', '2H1A']:
            #     self.price_algorithm = Constants.three_firm_agent[past_prices_tuple]
            # else:
            #     self.price_algorithm = Constants.two_firm_agent[past_prices_tuple]
            self.price_algorithm  = Constants.reservation_price  

    def calc_round_profit(self,):
        """

        A function that calculates all profits in a given market.
        """
        treatment = self.group_treatment

        # Create the set of all prices for the given treatment
        all_human_prices = [p.price for p in self.get_players()]
        if treatment in ['3H0A', '2H0A']:
            all_prices = all_human_prices
        else:
            algo_price = [self.price_algorithm]
            if treatment == '1H2A':
                all_prices = algo_price + algo_price + all_human_prices
            else:
                all_prices = algo_price + algo_price

        # Calculate the market outcome
        self.winning_price = min(all_prices)
        self.n_winners = len([price for price in all_prices if price == self.winning_price])

        for p in self.get_players():
            p.profit = self.calc_profit(p.price)
            # Accumulate profit if we played more than one round
            if self.round_number == 1:
                p.accumulated_profit = p.profit
            else:
                p.accumulated_profit = p.in_round(self.round_number - 1).accumulated_profit + p.profit

        self.profit_algorithm = self.calc_profit(self.price_algorithm)
        # Accumulated profit for the algorithm
        if self.round_number == 1:
            self.accumulated_profit_algorithm = self.profit_algorithm
        else:
            self.accumulated_profit_algorithm = self.in_round(self.round_number - 1).accumulated_profit_algorithm + self.profit_algorithm
        

    def calc_profit(self, price):
        """

        Calculate the profit for the given price
        and market information.
        """
        if price  > Constants.reservation_price:
            profit =  0
        elif price == self.winning_price:
            # Math ceil bcs of floating points
            # Int() would round down
            profit = math.ceil((1 / self.n_winners) * price * Constants.m_consumer)
        else:
            profit = 0
        return profit

class SharedBasePlayer(BasePlayer):
    class Meta:
        abstract = True

    price = models.IntegerField(
        min=Constants.lowest_price, max=Constants.maximum_price,
        doc= """Price player offers to sell product for"""
    )

    # Define all as Integer as they are points/tokens
    # Round specific profit and accumulated profit as points
    # I do not use CurrencyFields since those are a weird
    # otree invention.
    profit = models.IntegerField()
    accumulated_profit = models.IntegerField()

    # Final payoff is stored again
    final_payoff_sg = models.FloatField()

    def get_market_infos(self):
        """

        A function that returns the relevant market information
        for the participants in a given round as a tuple.
        (player_id, opponent_ids, opponent_prices)
        """
        treatment = self.participant.vars['group_treatment']

        # First the individual choice treatments
        # Algorithms are here always in second or third place
        if treatment == '1H1A':
            player_id = 1
            opponent_ids = [2]
            opponent_prices = [self.group.price_algorithm]
        elif treatment == '1H2A':
            player_id = 1
            opponent_ids = [2, 3]
            opponent_prices = [self.group.price_algorithm, self.group.price_algorithm]
        else:
            # If we are not in an indivdual choice treatment
            # the group will come into play.
            player_id = self.id_in_group
            opponents = self.get_others_in_group()
            opponent_ids_no_algo = [o.id_in_group for o in opponents]
            opponent_prices_no_algo = [o.price for o in opponents]
            
            if treatment in ['2H0A', '3H0A']:
                opponent_ids = opponent_ids_no_algo
                opponent_prices = opponent_prices_no_algo
            elif treatment == '2H1A':
                # Algorithm is always the last group member
                # TODO: Do I want to mention this in the instructions?
                opponent_ids = opponent_ids_no_algo + [3]
                opponent_prices = opponent_prices_no_algo + [self.group.price_algorithm]
        
        # Map the integer to letters from A to C
        player_letter = Constants.firma_id_map[player_id]
        opponent_letters = list(map(Constants.firma_id_map.get, opponent_ids))
        return (player_letter, opponent_letters, opponent_prices)
            
    def set_final_payoff(self):
        # We take the accumulated payoff from the last round we 
        # played.
        # This is stored as a fake-constant in the subsession, since it is a random draw
        # for each SuperGame and the different supergame apps inherit from this app
        last_played_round = self.subsession.this_app_constants()['round_number_draw']

        # Take the accumulated profit from the last round
        # IMPORTANT: Only use this method once the profit for the round has been calculated
        # using *set_profits_round* from the group method
        total_coins = self.in_round(last_played_round).accumulated_profit 
        final_payoff_sg = total_coins
        # Note, we do not save this to payoff as we will randomly select one of the 
        # super games for payoff.
        # Save the final accumulated payoff for the last subgame in the participant dict.
        self.sg_payoff_to_dict(sg_counter = self.subsession.this_app_constants()['super_game_count'],
                               final_payoff = total_coins)

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
        return {'round_number_draw': 11, 
                #'round_number_draw': 1, # for testing TODO: Remove
                'super_game_count': 1,
                'group_shuffle_by_size' : {
                    3: {'shuffle_structure_small': [[1,2,3], [4, 5, 6], [7, 8, 9]],
                       'shuffle_structure_medium': [[1,2,3], [4, 5, 6], [7, 8, 9],
                                                   [10, 11, 12], [13, 14, 15], [16, 17, 18]]
                    },
                    2: {'shuffle_structure_small': [[1,2], [3, 4], [5, 6]],
                        'shuffle_structure_medium': [[1,2], [3, 4], [5, 6],
                                                    [7,8], [9, 10], [11, 12]],
                        'shuffle_structure_big':  [[1,2], [3, 4], [5, 6],
                                                   [7,8], [9, 10], [11, 12],
                                                   [13,14], [15, 16], [17, 18]]
                    }
                }

                }

class Group(SharedBaseGroup):
    pass

class Player(SharedBasePlayer):
    pass


