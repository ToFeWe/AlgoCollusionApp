from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail


class PlayerBot(Bot):

    def play_round(self):
        if self.session.config['group_treatment'] =='recommendation':
            yield(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '0',
               'q_alg_how_sure': '1',
               'q_alg_no_recommendation': '2',
               'q_alg_relevant_other_player': '10'
            })
        assert "sozial angemessen wäre es in dieser Situation einen eigenen Preis" in self.html
        yield(pages.SurveyQuestionsAll,  {
            'q_all_other_players': '4',
            'q_all_communication': 'Ich weiß es nicht.',
            'q_socially_appropriate_10': 'sehr sozial unangemessen',
            'q_socially_appropriate_9' :'etwas sozial unangemessen',
            'q_socially_appropriate_1': 'sehr sozial angemessen'
        })
        yield(pages.SurveyQuestionsFalk, {
            'q_falk1': '0',
            'q_falk2': '10',
            'q_falk3': '5',
            'q_falk4': '4',
            'q_falk5': '9'
        })
        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 15,
            'q_gender': 'Divers',
            'q_study_field': 'Econ',  
            'q_semester': 12,
            'q_n_experiment': 4,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'

        })
        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 16,
            'q_gender': 'Divers',
            'q_study_field': 'Econ',  
            'q_semester': 0,
            'q_n_experiment': 4,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'

        })
        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 30,
            'q_gender': 'Divers',
            'q_study_field': 'Econ',  
            'q_semester': 1,
            'q_n_experiment': -1,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'

        })

        yield(pages.GeneralQuestions, {
            'q_age': 16,
            'q_gender': 'Divers',
            'q_study_field': 'Econ',  
            'q_semester': 12,
            'q_n_experiment': 4,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'
        })