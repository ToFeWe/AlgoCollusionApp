from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import math

class Introduction_1_Welcome(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()

        return additional_template_vars

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()

class Introduction_2_Main(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text

    def is_displayed(self):
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()

        return additional_template_vars

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()

class Introduction_3_Examples(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text

    def is_displayed(self):
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()

        return additional_template_vars

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()


class Introduction_4_Algos(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text
    
    def is_displayed(self):
        if self.participant.vars['is_dropout']:
            return False
        else:
            return self.group.group_treatment not in ['2H0A', '3H0A']

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()

        return additional_template_vars

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()

class Introduction_5_Procedure(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text

    def is_displayed(self):
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()

        return additional_template_vars

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()

class Quiz(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text

    form_model = 'player'
    form_fields =  ['q_how_many_customer',
                    'q_after_fixed_round',
                    'q_consumer_wtp',
                    'q_profit_1',
                    'q_profit_2',
                    'q_profit_3']

    def is_displayed(self):
        # TODO: Add defaults to DB for quiz? I dont need it I guess
        return not self.participant.vars['is_dropout']

    def vars_for_template(self):
        treatment =  self.group.group_treatment
        
        # Make label treatment specific
        if treatment in ['1H1A', '2H0A']:
            label_profit_1 = ('Sie sind Firma A und wählen einen Preis von 1, Firma B wählt einen Preis von 2.'
                              ' Was ist Ihr Gewinn in Talern in dieser Runde?')
            label_profit_2 = ('Sie sind Firma A und wählen einen Preis von 3, Firma B wählt einen Preis von 3.'
                              ' Was ist Ihr Gewinn in Talern in dieser Runde?')

        else:
            label_profit_1 = ('Sie sind Firma A und wählen einen Preis von 1, Firma B wählt einen Preis von 2,' +
                             ' Firma C wählt einen Preis von 3. Was ist Ihr Gewinn in Talern in dieser Runde?')
            label_profit_2 = ('Sie sind Firma A und wählen einen Preis von 3, Firma B wählt einen Preis von 3,' +
                              ' Firma C wählt einen Preis von 3. Was ist Ihr Gewinn in Talern in dieser Runde?')

        additional_template_vars = self.group.get_additional_template_variables()
        
        context = {
            'treatment': treatment,
            'label_profit_1': label_profit_1,
            'label_profit_2': label_profit_2
        }
        context.update(additional_template_vars)
        
        return context

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()


class Quiz_results(Page):
    timeout_seconds = Constants.timeout_hard
    timer_text = Constants.timeout_text

    def is_displayed(self):    
        if self.participant.vars['is_dropout']:
            return False
        else:
            # Only show the review page if the participant had stuff wrong
            return self.player.three_times_wrong

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()

        return additional_template_vars

    def before_next_page(self):
        timeout_happened = self.timeout_happened
        if timeout_happened:
            self.player.record_dropout()

page_sequence = [
    Introduction_1_Welcome,
    Introduction_2_Main,
    Introduction_3_Examples,
    Introduction_4_Algos,
    Introduction_5_Procedure,
    Quiz,
    Quiz_results
]