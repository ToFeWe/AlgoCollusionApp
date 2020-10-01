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
    form_fields =  ['q_how_many_customer',
                    'q_after_fixed_round',
                    'q_profit_1',
                    'q_profit_2',
                    'q_profit_3']
    
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        # Group treatment stored in participant.vars of
        # first group member.
        treatment =  self.participant.vars['group_treatment']
        
        # Make label treatment specific
        if treatment in ['1H1A', '2H0A']:
            label_profit_1 = ('Sie sind Firma A und wählen einen Preis von 1, Firma B wählt einen Preis von 2.',
                              ' Was ist Ihr Gewinn in Talern in dieser Runde?')
            label_profit_2 = ('Sie sind Firma A und wählen einen Preis von 3, Firma B wählt einen Preis von 3.',
                              ' Was ist Ihr Gewinn in Talern in dieser Runde?')

        else:
            label_profit_1 = ('Sie sind Firma A und wählen einen Preis von 1, Firma B wählt einen Preis von 2,' +
                             ' Firma C wählt einen Preis von 3. Was ist Ihr Gewinn in Talern in dieser Runde?')
            label_profit_2 = ('Sie sind Firma A und wählen einen Preis von 3, Firma B wählt einen Preis von 3,' +
                              ' Firma C wählt einen Preis von 3. Was ist Ihr Gewinn in Talern in dieser Runde?')

        return {
            'treatment': treatment,
            'label_profit_1': label_profit_1,
            'label_profit_2': label_profit_2
        }


page_sequence = [
    Introduction_1,
    Introduction_2,
    Introduction_3,
    Introduction_4,
    Quiz,
]