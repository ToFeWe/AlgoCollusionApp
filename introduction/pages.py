from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction_1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction_2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        exchange_rate = 1 / self.session.config['real_world_currency_per_point']
        coins_in_euro = 844 / exchange_rate

        return {
            'exchange_rate': exchange_rate,
            'show_up_fee': self.session.config['participation_fee'],
            'coins_in_euro': coins_in_euro,
            'coins_in_euro_rounded': round(coins_in_euro, 1)
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

class Algorithm_Introduction(Page):
    def is_displayed(self):
        treatment =  self.participant.vars['group_treatment']
        return treatment == 'recommendation' and self.round_number == 1


class NewGame(Page):
    pass
 


class Quiz(Page):
    form_model = 'player'

    def get_form_fields(self):
        treatment =  self.participant.vars['group_treatment']
        if treatment == 'baseline':
            return ['q_how_many_customer',
                    'q_after_fixed_round',
                    'q_profit_1',
                    'q_profit_2',
                    'q_profit_3']
        else:
            return ['q_how_many_customer',
                    'q_after_fixed_round',
                    'q_profit_1',
                    'q_profit_2',
                    'q_profit_3',
                    'q_goal_alg']
    
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
    Algorithm_Introduction,
    Quiz,
]