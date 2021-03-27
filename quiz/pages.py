from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class General(Page):
    form_model = 'player'
    form_fields = ['q_age', 'q_gender', 'q_study_level', 'q_study_field',
                   'q_semester', 'q_n_experiment', 
                   'q_abitur', 'q_math', 'q_budget', 'q_spending']

    def is_displayed(self):
        #TODO: Should I add timeouts here too and record dropouts?
        if self.participant.vars['is_dropout']:
            return False
        else:
            return True
        
class Falk(Page):
    form_model = 'player'
    form_fields = ['q_falk_risk', 'q_falk_time',
                   'q_falk_trust', 'q_falk_neg_rec',
                   'q_falk_pos_rec', 'q_falk_altruism']

    def is_displayed(self):
        if self.participant.vars['is_dropout']:
            return False
        else:
            return True


page_sequence = [General, Falk]
