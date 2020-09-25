from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import math

class Introduction_1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction_2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        exchange_rate = 1 / self.session.config['real_world_currency_per_point']
        coins_in_euro = 465 / exchange_rate

        return {
            'exchange_rate': int(exchange_rate), # Int to avoid comma
            'show_up_fee': self.session.config['participation_fee'],
            'coins_in_euro': coins_in_euro,
            'coins_in_euro_rounded': math.ceil(coins_in_euro * 10) / 10 # Round up first decimal digit
        }

class Introduction_3(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction_4(Page):
    def is_displayed(self):
        return self.round_number == 1
        
    def vars_for_template(self):
        return {
            'show_up_fee': self.session.config['participation_fee']
        }

class Quiz(Page):
    form_model = 'player'

    def get_form_fields(self):
        treatment =  self.participant.vars['group_treatment']
        return ['q_how_many_customer',
                'q_after_fixed_round',
                'q_profit_1',
                'q_profit_2',
                'q_profit_3']
        #TODO: Maybe ask how many players are an algo
        # Ask who receives payoff from algorithm 
    
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        # Group treatment stored in participant.vars of
        # first group member.
        treatment =  self.participant.vars['group_treatment']
        
        return {
            'treatment': treatment
        }


page_sequence = [
    Introduction_1,
    Introduction_2,
    Introduction_3,
    Introduction_4,
    #Quiz,
]