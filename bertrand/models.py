from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy as np

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
                    else:
                        shuffle_structure = self.this_app_constants()['group_shuffle_by_size'][group_size]['shuffle_structure_big']
            else:
                # In the individual choice treatments, we do not have a group matching
                shuffle_structure = self.get_group_matrix()
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
            # Assign the treatment to each player in the session
            # Note that we store it in the *treatment* field in the 
            # first round but also in the participant variables of
            # the first participant in the group to access it across rounds. 
            for p in self.get_players():
                # *group_treatment* has to be specified in the session config
                treatment_draw = self.session.config['group_treatment']
                
                # Store it in the variable *group_treatment* for first round for the group
                p.group_treatment = treatment_draw

                # Furthermore, store it in the participant variables for the each player in each
                # group to access it accross rounds.
                p.participant.vars['group_treatment'] = treatment_draw
                
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
    final_payoff_sg = models.FloatField()

    #### NOTE: Usually we would define the following variables ########
    #### in the Group model. This is not possible as some treatments ##
    #### are indivdiual choice (with Algos only) ######################
    # Market specific variables for each round in the given SG
    winning_price = models.IntegerField()
    winner_profit = models.IntegerField()
    n_winners = models.IntegerField()

    # Treatment storage
    group_treatment = models.StringField()


    # Prices of the algorithm(s)
    # Note that in markets with two algorithms,
    # the price of those algorithms must be
    # symmetric, given its the same with the same input.
    price_algorithm = models.IntegerField()


    def get_market_infos(self):
        """

        A function that returns the relevant market informations
        for the participants in a given round as a tuple.
        (player_id, opponent_ids, opponent_prices)
        """
        treatment = self.participant.vars['group_treatment']

        # First the individual choice treatments
        # Algorithms are here always in second or thrid place
        if treatment == '1H1A':
            player_id = 1
            opponent_ids = [2]
            opponent_prices = [self.price_algorithm]
        elif treatment == '1H2A':
            player_id = 1
            opponent_ids = [2, 3]
            opponent_prices = [self.price_algorithm, self.price_algorithm]
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
                opponent_prices = opponent_prices_no_algo + [self.price_algorithm]
        
        # Map the integer to letters from A to C
        player_letter = Constants.firma_id_map[player_id]
        opponent_letters = list(map(Constants.firma_id_map.get, opponent_ids))
        return (player_letter, opponent_letters, opponent_prices)


    def set_algo_price(self):
        """
        
        A function to get the price of the algortihmic player
        in the given round given the prices that haven been played
        in the last round.
        """
        treatment = self.participant.vars['group_treatment']
        past_algo_price = self.in_previous_rounds()[-1].price_algorithm
        past_human_price = self.in_previous_rounds()[-1].price
        if treatment == '1H2A':
            past_prices_tuple = (past_algo_price, past_algo_price, past_human_price)
        elif treatment == '1H1A':
            past_prices_tuple = (past_algo_price, past_human_price)
        elif treatment == '2H1A':
            # Note that in the 2H1A treatment we have to use the whole
            # group element to obtain the algorithmic price for the round.
            # The reason is that the order of prices matters when creating the 
            # past_prices_tuple. We use the structure provided by the 
            # group s.t. the algorihmic price is the same for each group
            # member (as it should be).
            all_group_members = self.group.get_players()
            past_all_human_prices = (p.in_previous_rounds()[-1].price for p in all_group_members)
            # Like this the person who is "first" in the group is also first  after the algo 
            # in the *past_prices_tuple*.
            past_prices_tuple = (past_algo_price,) + past_all_human_prices
        
        # TODO: Import algorithms and save to Constants
        # # differ which algorithm to use by treatment (3 or 2 firm market)
        # if treatment in ['1H2A', '2H1A']:
        #     self.price_algorithm = Constants.three_firm_agent[past_prices_tuple]
        # else:
        #     self.price_algorithm = Constants.two_firm_agent[past_prices_tuple]
        self.price_algorithm  = Constants.maximum_price        

    def set_profits_round(self, treatment):
        """
        
        A function to set the payoffs for a specific round.
        Note that usually this would be a group method. Given
        that we have some treatments with individual choice,
        it is however easier to implement it here.
        """

        # First for the treatments with only one human
        if treatment == '1H1A':
            all_prices = [self.price_algorithm, self.price]
        elif treatment == '1H2A':
            all_prices = [self.price_algorithm, self.price_algorithm, self.price]
        else:
            # Now for the treatments where we acutally have a group
            other_group_members = self.get_others_in_group()
            other_prices = [p.price for p in other_group_members]
            if treatment == '2H1A':
                all_prices = [self.price_algorithm] + [self.price] + other_prices
            else: # 2H0A and 3H0A
                all_prices = [self.price] + other_prices

        # Calculate the profit for the participant in the given round
        self.profit, self.winning_price, self.n_winners = calc_round_profit(p_i=self.price,
                                                                            all_prices = all_prices)
    
        if self.price == self.winning_price:
            self.is_winner = True
                        
        # Accumulate profit if we played more than one round
        if self.round_number == 1:
            self.accumulated_profit = self.profit
        else:
            self.accumulated_profit = self.in_round(self.round_number - 1).accumulated_profit + self.profit
    
    def calc_round_profit(self, p_i, all_prices):
        """

        A function that takes the price of the participant, *p_i*,
        and *all_prices* in the market and returns the profit
        for the participant, the market price and 
        the number of firms that played this market price as a tuple
        """
        winning_price = min(all_prices)
        n_winning_price = len([price for price in all_prices if price == winning_price])

        if p_i  > Constants.reservation_price:
            profit =  0
        elif p_i == winning_price:
            profit = int((1 / n_winning_price) * p_i * Constants.m_consumer)
        else:
            profit = 0
        return (profit, winning_price, n_winning_price)
        
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


