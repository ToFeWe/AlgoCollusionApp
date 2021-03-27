from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail

import random

class SharedPlayerBot(Bot):
    # TODO: Test Time out case
    cases = [ 'specific_prices']#'monopoly',

    def play_round(self):
        case = self.case
        treatment = self.session.config['group_treatment']
        n_players = 2 if treatment in ['2H0A', '1H1A'] else 3

        if self.round_number == 1:
            self.test_stranger_matching()
            yield(pages.StartExperiment)
            # Check in the first round if the price bounds are correct
            yield SubmissionMustFail(pages.Decide, {'price': -1}, error_fields=['price'])
            yield SubmissionMustFail(pages.Decide, {'price': 6}, error_fields=['price']) 
            yield SubmissionMustFail(pages.Decide, {'price': 3.2}, error_fields=['price']) 

        if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:
            # Check if instructions are shown on the page
            assert "Firmen entscheiden in jeder Runde erneut" in self.html
            if treatment in ['1H1A', '1H2A', '2H1A']:
                assert "Marktentscheidungen durch Algorithmen" in self.html
            else:
                assert "Marktentscheidungen durch Algorithmen" not in self.html

            if case == 'monopoly':
                yield(pages.Decide, {'price': Constants.reservation_price})
                # Conditional on full cooperation algorithms plays monopoly price too
                assert self.player.profit == int(4 * 60 / n_players)
            elif case == 'specific_prices':
                # Play a specific price cycle and check if the outcome matches
                # our expectation.
                price = 4
                if self.round_number == 2:
                    price = 3
                elif self.round_number == 3:
                    price = 1
                elif self.round_number == 4:
                    price = 3
                elif self.round_number == 5:
                    price = 4
                yield(pages.Decide, {'price': price})
                self.check_specific_prices(treatment=treatment)
            if n_players == 3:
                assert 'Firma C' in self.html
            else:
                assert 'Firma C' not in self.html

            # If the player won the market, she must have have made a profit
            if self.player.price == self.group.winning_price:
                assert str(int(self.group.winning_price/self.group.n_winners * Constants.m_consumer)) in self.html
            assert str(int(self.player.price)) in self.html
            assert str(int(self.group.winning_price)) in self.html

            yield(pages.RoundResults)
            
            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
                # Check if the total profit is shown correctly
                accumulated_payoff_in_app = sum([p_in_r.profit for p_in_r in self.player.in_all_rounds()])
                assert str(int(accumulated_payoff_in_app)) in self.html, "Not there"
                
                # And if it has been saved correctly
                sg_counter = self.subsession.this_app_constants()['super_game_count']
                key_name = "final_payoff_sg_" + str(sg_counter)        
                assert accumulated_payoff_in_app == self.participant.vars[key_name]

                assert "insgesamt einen Gewinn von <b>{} Taler".format(int(accumulated_payoff_in_app)) in self.html
                if sg_counter == 1 or sg_counter == 2:
                    assert "Sie spielen jetzt vom gleichen Spiel einen neuen Durchgang" in self.html
                else:
                    assert "Dies war der letzte Durchgang" in self.html
                assert "dies die letzte Runde des {}. Durchgangs".format(self.subsession.this_app_constants()['super_game_count']) in self.html
                yield(pages.EndSG)

    def check_specific_prices(self, treatment):
        err_msg_price = 'Price is wrong!'
        err_msg_profit = 'Profit is wrong'
        if treatment == '1H1A':
            if self.round_number == 1:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 120, err_msg_profit
                assert self.player.profit == 120, err_msg_profit
            elif self.round_number == 2:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 180, err_msg_profit
            elif self.round_number == 3:
                assert self.group.price_algorithm == 1, err_msg_price
                assert self.group.profit_algorithm == 30, err_msg_profit
                assert self.player.profit == 30, err_msg_profit
            elif self.round_number == 4:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 180, err_msg_profit
            elif self.round_number == 5:
                assert self.group.price_algorithm == 1, err_msg_price
                assert self.group.profit_algorithm == 60, err_msg_profit
                assert self.player.profit == 0, err_msg_profit
            else:
                assert self.group.price_algorithm == 1, err_msg_price
                assert self.group.profit_algorithm == 60, err_msg_price
                assert self.player.profit == 0, err_msg_profit


        elif treatment == '2H1A':
            if self.round_number == 1:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 80, err_msg_profit
                assert self.player.profit == 80, err_msg_profit
            elif self.round_number == 2:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 90, err_msg_profit
            elif self.round_number == 3:
                assert self.group.price_algorithm == 1, err_msg_price
                assert self.group.profit_algorithm == 20, err_msg_profit
                assert self.player.profit == 20, err_msg_profit
            elif self.round_number == 4:
                assert self.group.price_algorithm == 0, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 0, err_msg_profit
            elif self.round_number == 5:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 80, err_msg_profit
                assert self.player.profit == 80, err_msg_profit
            else:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 80, err_msg_profit
                assert self.player.profit == 80, err_msg_profit
        elif treatment == '1H2A':
            if self.round_number == 1:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 80, err_msg_profit
                assert self.player.profit == 80, err_msg_profit
            elif self.round_number == 2:
                assert self.group.price_algorithm == 4, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 180, err_msg_profit
            elif self.round_number == 3:
                assert self.group.price_algorithm == 1, err_msg_price
                assert self.group.profit_algorithm == 20, err_msg_profit
                assert self.player.profit == 20, err_msg_profit
            elif self.round_number == 4:
                assert self.group.price_algorithm == 0, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 0, err_msg_profit
            elif self.round_number == 5:
                assert self.group.price_algorithm == 2, err_msg_price
                assert self.group.profit_algorithm == 60, err_msg_profit
                assert self.player.profit == 0, err_msg_profit
            elif self.round_number == 6:
                assert self.group.price_algorithm == 0, err_msg_price
                assert self.group.profit_algorithm == 0, err_msg_profit
                assert self.player.profit == 0, err_msg_profit
            else:
                assert self.group.price_algorithm == 1, err_msg_price
                assert self.group.profit_algorithm == 30, err_msg_profit
                assert self.player.profit == 0, err_msg_profit
                #TODO: Add accumulated profit assertion
        elif treatment == '2H0A':
            assert self.group.price_algorithm == None, 'No Algo in this treatment.'
            assert self.group.profit_algorithm == None, 'No Algo in this treatment.'
            if self.round_number == 1:
                assert self.player.profit == 120, err_msg_profit
            elif self.round_number == 2:
                assert self.player.profit == 90, err_msg_profit
            elif self.round_number == 3:
                assert self.player.profit == 30, err_msg_profit
            elif self.round_number == 4:
                assert self.player.profit == 90, err_msg_profit
            else:
                assert self.player.profit == 120, err_msg_profit
        elif treatment == '3H0A':
            assert self.group.price_algorithm == None, 'No Algo in this treatment.'
            assert self.group.profit_algorithm == None, 'No Algo in this treatment.'
            if self.round_number == 1:
                assert self.player.profit == 80, err_msg_profit
            elif self.round_number == 2:
                assert self.player.profit == 60, err_msg_profit
            elif self.round_number == 3:
                assert self.player.profit == 20, err_msg_profit
            elif self.round_number == 4:
                assert self.player.profit == 60, err_msg_profit
            else:
                assert self.player.profit == 80, err_msg_profit

    def test_stranger_matching(self):
        """
        
        A function to test the grouping matrix supplied to
        oTree in each super game. The matrix has been copied 
        from the constants as oTree is limiting me to do
        it in another way.
        """
        matricies = {
            1:  {
                        3: {'shuffle_structure_small': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                            'shuffle_structure_medium': [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                                                        [10, 11, 12], [13, 14, 15], [16, 17, 18]]
                            },
                        2: {'shuffle_structure_small': [[1, 2], [3, 4], [5, 6]],
                            'shuffle_structure_medium': [[1, 2], [3, 4], [5, 6],
                                                        [7, 8], [9, 10], [11, 12]],
                            'shuffle_structure_big': [[1, 2], [3, 4], [5, 6],
                                                    [7, 8], [9, 10], [11, 12],
                                                    [13, 14], [15, 16], [17, 18]]
                            }
                    },
            2: {
                        3: {'shuffle_structure_small': [[1,5,9], [4, 8, 3], [7, 2, 6]],
                            'shuffle_structure_medium': [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                                                        [10, 14, 18], [13, 17, 12], [16, 11, 15]]
                            },
                        2: {'shuffle_structure_small': [[1,6], [3, 2], [5, 4]],
                            'shuffle_structure_medium': [[1,6], [3, 2], [5, 4],
                                                        [7,12], [9, 8], [11, 10]],
                            'shuffle_structure_big':  [[1,6], [3, 2], [5, 4],
                                                    [7,12], [9, 8], [11, 10],
                                                    [13,18], [15, 14], [17, 16]]
                        }
                },
            3: {
                        3 : {'shuffle_structure_small': [[1, 6, 8], [4, 9, 2], [7, 3, 5]],
                            'shuffle_structure_medium': [[1, 6, 8], [4, 9, 2], [7, 3, 5],
                                                        [10, 15, 17], [13, 18, 11], [16, 12, 14]]
                            },
                        2: {'shuffle_structure_small': [[1,4], [3, 6], [5, 2]],
                            'shuffle_structure_medium': [[1,4], [3, 6], [5, 2],
                                                        [7,10], [9, 12], [11, 8]],
                            'shuffle_structure_big':  [[1,4], [3, 6], [5, 2],
                                                    [7,10], [9, 12], [11, 8],
                                                    [13,16], [15, 18], [17, 14]]
                        }
                    } 
        }
        # Do those test for 2 and 3 player treatment
        for n_participants in [2,3]:
            shuffel_structures = matricies[1][n_participants].keys()
            # And for all session sizes
            for structure in shuffel_structures:
                all_participants =  [item for sublist in matricies[1][n_participants][structure] for item in sublist]
                check_dict = {p:list() for p in all_participants}
                # Across all super games
                for sg in [1,2,3]:
                    all_lists = matricies[sg][n_participants][structure]
                    # And for all participants
                    for p in all_participants:
                        for l in all_lists:
                            if p in l:
                                # Saving the past participants
                                check_dict[p].extend([i for i in l if i !=p])
                for p in check_dict.keys():
                    # Check if the groups number are different across super games
                    assert len(check_dict[p]) == len(set(check_dict[p])), "Perfect stranger matching matrix is wrong"

class PlayerBot(SharedPlayerBot):
    pass