from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import math

class PlayerBot(Bot):
    def play_round(self):
        paid_sg_string = str(self.player.paid_sg)
        assert int(paid_sg_string) in [1,2,3]

        key_payoff_sg = 'final_payoff_sg_' + paid_sg_string
        assert str(self.participant.vars['final_payoff_sg_1']) in self.html
        assert str(self.participant.vars['final_payoff_sg_2']) in self.html
        assert str(self.participant.vars['final_payoff_sg_3']) in self.html

        # 130 points are one euro
        final_coins_in_euro = self.participant.vars[key_payoff_sg] / 130
        final_coins_in_euro_rounded = round(final_coins_in_euro * 100) / 100

        assert "Bonus für Ihr pünktliches Erscheinen" in self.html
        assert "Gesamtgewinn" in self.html
        assert "130" in self.html # Conversion rate in pre reg
        # Replace . with , given the formating of django with the german language code
        assert str(final_coins_in_euro_rounded).replace('.',',') in self.html #SG Payoff
        assert str(final_coins_in_euro_rounded + 4.0).replace('.',',') in self.html # SG payoff + show-up 
        

        assert self.participant.payoff.to_real_world_currency(self.session) + 4 == self.participant.payoff_plus_participation_fee()
            
        assert str(paid_sg_string) + '. Spiel ausgezahlt' in self.html
        
        yield Submission(pages.FinalResults, check_html=False)
