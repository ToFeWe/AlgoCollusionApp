from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail

import random

class SharedPlayerBot(Bot):
    cases = ['monopoly']
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
            yield(pages.RoundResults)
            
            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
                yield(pages.EndSG)



class PlayerBot(SharedPlayerBot):
    pass  