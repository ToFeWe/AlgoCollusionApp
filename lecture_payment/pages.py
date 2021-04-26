from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MailPage(Page):
    form_model = 'player'
    form_fields = ['mail']

    def is_displayed(self):
        # Page is only required if we did not use
        # pass the orsee id via the participant label and if the
        # participant is not a dropout.
        return not self.participant.vars['is_dropout']

    def before_next_page(self):
        self.participant.label = self.player.mail

class FinalResults(Page):
    def is_displayed(self):
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        # Set the payoff as the randomly selected super game
        paid_sg_string = str(self.player.paid_sg)
        key_payoff_sg = 'final_payoff_sg_' + paid_sg_string
        self.player.payoff = self.participant.vars[key_payoff_sg]

        # save to dict for admin report
        self.participant.vars['final_money_with_show_up'] =  self.participant.payoff_plus_participation_fee(),
        self.participant.vars['final_money_no_show_up'] =  self.participant.payoff.to_real_world_currency(self.session)

        return {
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee'],
            'final_money_with_show_up' : self.participant.payoff_plus_participation_fee(),
            'final_money_no_show_up': self.participant.payoff.to_real_world_currency(self.session),
            'payoff_coins': self.participant.payoff,
            'payoff_sg_1': self.participant.vars['final_payoff_sg_1'],
            'payoff_sg_2': self.participant.vars['final_payoff_sg_2'],
            'payoff_sg_3': self.participant.vars['final_payoff_sg_3'],
            'paid_sg': self.player.paid_sg,
            'payoff_plus_participation_fee': self.participant.payoff_plus_participation_fee()
        }

class DropOut(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout']


page_sequence = [MailPage, FinalResults, DropOut]
