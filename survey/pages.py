from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class SurveyQuestionsAlg(Page):    
    form_model = 'player'
    form_fields = ['q_alg_helpful', 'q_alg_no_recommendation',
                   'q_alg_relevant_other_player', 'q_alg_improve', 'q_alg_comments']
    def is_displayed(self):
        treatment = self.participant.vars['group_treatment']
        return treatment != 'baseline'


class SurveyQuestionsFalk(Page):    
    form_model = 'player'
    form_fields = ['q_falk1', 'q_falk2',
                   'q_falk3', 'q_falk4',
                   'q_falk5']


class GeneralQuestions(Page):    
    form_model = 'player'
    form_fields = ['q_age', 'q_gender', 'q_study_level', 'q_student', 'q_study_field',
                   'q_semester', 'q_n_experiment', 'q_similar_experiment', 'q_other_notes']

page_sequence = [
    SurveyQuestionsAlg,
    SurveyQuestionsFalk,
    GeneralQuestions
]
