from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import math

class FinalResults(Page):    
    def vars_for_template(self):

        # Set the payoff as the randomly selected super game
        payed_sg_string = str(self.subsession.payed_sg)
        key_payoff_sg = 'final_payoff_sg_' + payed_sg_string
        self.player.payoff = self.participant.vars[key_payoff_sg]


        money_not_rounded_no_show_up = self.player.payoff * self.session.config['real_world_currency_per_point']
        self.player.final_money_no_show_up = float(math.ceil(money_not_rounded_no_show_up * 10) / 10)
        self.player.final_money_with_show_up = self.player.final_money_no_show_up + float(self.session.config['participation_fee'])

        # Also write it to the participant dict as we use it for the admin report
        self.participant.vars['final_money_with_show_up'] = self.player.final_money_with_show_up
        self.participant.vars['final_money_no_show_up'] = self.player.final_money_no_show_up

        return {
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee'],
            'final_money_with_show_up' : self.player.final_money_with_show_up,
            'final_money_no_show_up': self.player.final_money_no_show_up,
            'payoff_coins': self.participant.payoff,
            'payoff_sg_1': self.participant.vars['final_payoff_sg_1'],
            'payoff_sg_2': self.participant.vars['final_payoff_sg_2'],
            'payoff_sg_3': self.participant.vars['final_payoff_sg_3'],
            'payed_sg': self.subsession.payed_sg
        }


page_sequence = [
    FinalResults
    ]
