from otree.api import Currency as c, currency_range, expect, Submission
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if self.participant.vars['is_dropout']:
            yield Submission(pages.DropOut, check_html=False)
        else:
            if self.participant.label is None:
                yield pages.OrseeID, dict(orsee_id="test-id")
            expect(str(self.participant.payoff_plus_participation_fee()), "in", self.html)

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

            # Replace . with , given the formating of django with the German language code
            # Also remove trailing zeros from floating
            assert f"{final_coins_in_euro_rounded:g}".replace('.',',') in self.html #SG Payoff
            assert f"{final_coins_in_euro_rounded + 4:g}".replace('.',',') in self.html # SG payoff + show-up 

            assert self.participant.payoff.to_real_world_currency(self.session) + 4 == self.participant.payoff_plus_participation_fee()
                
            assert str(paid_sg_string) + '. Spiel ausgezahlt' in self.html
            
            yield Submission(pages.FinalResults, check_html=False)
