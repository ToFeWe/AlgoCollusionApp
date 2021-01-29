from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail

import random

class SharedPlayerBot(Bot):
    cases = [ 'specific_prices']#'monopoly',
    def play_round(self):
        case = self.case
        treatment = self.session.config['group_treatment']
        n_players = 2 if treatment in ['2H0A', '1H1A'] else 3
            
        if self.round_number == 1:
            yield(pages.StartExperiment)

        if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:
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
            yield(pages.RoundResults)
            
            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
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

class PlayerBot(SharedPlayerBot):
    pass