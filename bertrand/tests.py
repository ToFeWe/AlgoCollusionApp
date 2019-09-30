from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class SharedPlayerBot(Bot):
    cases = ['follow']
    # , 'hip_hop_player', 'deviation'
    def play_round(self):
        #case = self.case
        #if case == 'follow':
        if self.round_number == 1:
            yield(pages.StartExperiment)
        if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:
            yield(pages.Decide, {'price': 10})
            yield(pages.RoundResults)
            yield(pages.HistoryResults)

        if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
            yield(pages.EndRound)


class PlayerBot(SharedPlayerBot):
    pass