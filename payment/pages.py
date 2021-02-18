from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import math

class FinalResults(Page):
    def is_displayed(self):
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        # Set the payoff as the randomly selected super game
        payed_sg_string = str(self.player.payed_sg)
        key_payoff_sg = 'final_payoff_sg_' + payed_sg_string
        self.player.payoff = self.participant.vars[key_payoff_sg]


        money_not_rounded_no_show_up = self.participant.vars[key_payoff_sg] * self.session.config['real_world_currency_per_point']
        self.player.final_money_no_show_up = float(math.ceil(money_not_rounded_no_show_up * 10) / 10)
        self.player.final_money_with_show_up = self.player.final_money_no_show_up + float(self.session.config['participation_fee'])
        
        # After Corona participants received an additonal 4 Euros for their participation to substitute for their loss of income.
        # This was only announced at the last page of the experiment and hence, did not change the results of any treatments.
        self.player.final_money_with_show_up_and_corona = self.player.final_money_with_show_up + float(self.session.config['corona_bonus_after_end'])

        # Also write it to the participant dict as we use it for the admin report
        self.participant.vars['final_money_with_show_up'] = self.player.final_money_with_show_up
        self.participant.vars['final_money_no_show_up'] = self.player.final_money_no_show_up
        self.participant.vars['final_money_with_show_up_and_corona'] = self.player.final_money_with_show_up_and_corona

        return {
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee'],
            'corona_bonus_after_end' : self.session.config['corona_bonus_after_end'],
            'final_money_with_show_up' : self.player.final_money_with_show_up,
            'final_money_no_show_up': self.player.final_money_no_show_up,
            'final_money_with_show_up_and_corona': self.player.final_money_with_show_up_and_corona,
            'payoff_coins': self.participant.payoff,
            'payoff_sg_1': self.participant.vars['final_payoff_sg_1'],
            'payoff_sg_2': self.participant.vars['final_payoff_sg_2'],
            'payoff_sg_3': self.participant.vars['final_payoff_sg_3'],
            'payed_sg': self.player.payed_sg
        }

class Payment(Page):
    def is_displayed(self):
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        return {
            'final_money_with_show_up_and_corona': self.player.final_money_with_show_up_and_corona
        }

class DropOut(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout']

page_sequence = [
    FinalResults,
    Payment,
    DropOut
    ]
