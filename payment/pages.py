from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FinalResults(Page):    
    def vars_for_template(self):
        return {
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee'],
            'final_payoff_euro' : float(self.participant.payoff_plus_participation_fee())


        }


page_sequence = [
    FinalResults
    ]
