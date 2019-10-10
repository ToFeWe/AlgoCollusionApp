from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        payed_sg_string = str(self.subsession.payed_sg)
        key_payoff_sg = 'final_payoff_sg_' + payed_sg_string
        assert str(self.participant.vars[key_payoff_sg]) in self.html
        assert str(payed_sg_string) + '. Spiel ausgezahlt' in self.html
        yield Submission(pages.FinalResults, check_html=False)