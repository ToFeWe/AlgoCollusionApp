from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class BeforeSurvey(Page):    
    pass

class SurveyQuestionsAlg(Page):    
    form_model = 'player'
    form_fields = ['q_alg_helpful', 'q_alg_how_sure', 'q_alg_no_recommendation',
                   'q_alg_relevant_other_player']
    def is_displayed(self):
        treatment = self.participant.vars['group_treatment']
        return treatment == 'recommendation'


class SurveyQuestionsAll(Page):    
    form_model = 'player'
    form_fields = ['q_all_other_players', 'q_all_communication']


class GeneralQuestions(Page):    
    form_model = 'player'
    form_fields = ['q_age', 'q_gender', 'q_study_field',
                   'q_semester', 'q_n_experiment', 'q_similar_experiment']

page_sequence = [
    BeforeSurvey,
    SurveyQuestionsAlg,
    SurveyQuestionsAll,
    GeneralQuestions
]
