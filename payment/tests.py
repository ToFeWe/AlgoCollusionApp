from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import math

class PlayerBot(Bot):
    def play_round(self):
        payed_sg_string = str(self.player.payed_sg)
        assert int(payed_sg_string) in [1,2,3]

        key_payoff_sg = 'final_payoff_sg_' + payed_sg_string
        assert str(self.participant.vars['final_payoff_sg_1']) in self.html
        assert str(self.participant.vars['final_payoff_sg_2']) in self.html
        assert str(self.participant.vars['final_payoff_sg_3']) in self.html

        # 100 points are one euro
        final_coins_in_euro = self.participant.vars[key_payoff_sg] * 0.01
        final_coins_in_euro_rounded = math.ceil(final_coins_in_euro * 10) / 10

        # Replace . with , given the formating of django with the german langauge code
        assert "Bonus für Ihr pünktliches Erscheinen" in self.html
        assert "Coronebedingter Extrabonus" in self.html
        assert "Gesamtgewinn" in self.html
        assert "Paypal" in self.html


        assert str(final_coins_in_euro_rounded).replace('.',',') in self.html #SG Payoff
        assert str(final_coins_in_euro_rounded + 4.0 + 4.0).replace('.',',') in self.html # SG payoff + show-up + Corona
        

        assert self.player.final_money_no_show_up + 4 == self.player.final_money_with_show_up
        assert self.player.final_money_no_show_up + 4 + 4 == self.player.final_money_with_show_up_and_corona
            
        assert str(payed_sg_string) + '. Spiel ausgezahlt' in self.html
        
        yield Submission(pages.FinalResults, check_html=False)