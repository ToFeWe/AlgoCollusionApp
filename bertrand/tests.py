from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    cases = ['follow']
    # , 'hip_hop_player', 'deviation'
    def play_round(self):
        #case = self.case
        #if case == 'follow':
        if self.round_number == 1:
            yield(pages.Introduction)
            yield(pages.Explanation)
            if self.participant.vars['group_treatment'] == 'baseline':
                yield (pages.Quiz, {'q_bertrand_1': 1, 
                                        'q_recommendation_1': 'bla'})
            else:
                yield (pages.Quiz, {'q_bertrand_1': 1, 
                            'q_recommendation_1': 'bla',
                            'q_recommendation_2': 'bla'})
            yield(pages.StartExperiment)
        if self.session.vars['playing'] is True:
            yield(pages.Decide, {'price': 10})
            yield(pages.RoundResults)
            yield(pages.HistoryResults)

        if self.round_number == Constants.fixed_rounds:
            yield(pages.LastFixedRound)
