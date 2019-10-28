from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail
import numpy as np

class PlayerBot(Bot):

    def play_round(self):
        # We test on each page the extrem cases on the likert scale
        # and else randomly
        likert_choices = [str(i) for i in range(11)]
        
        if self.session.config['group_treatment'] =='recommendation':
            yield SubmissionMustFail(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '-1',
               'q_alg_how_sure': np.random.choice(likert_choices),
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '10',
               'q_alg_comments': 'lala',
               'q_alg_improve': 'testets'
            })

            yield SubmissionMustFail(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '0',
               'q_alg_how_sure': np.random.choice(likert_choices),
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '11',
               'q_alg_comments': 'lala',
               'q_alg_improve': 'testets'
            })
            yield(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '0',
               'q_alg_how_sure': np.random.choice(likert_choices),
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '10',
               'q_alg_comments': 'lala',
               'q_alg_improve': 'testets'
            })
        assert "sozial angemessen wäre es in dieser Situation einen eigenen Preis" in self.html
        yield SubmissionMustFail(pages.SurveyQuestionsAll,  {
            'q_all_other_players': '-1',
            'q_all_communication': 'Ich weiß es nicht.',
            'q_socially_appropriate_10': 'sehr sozial unangemessen',
            'q_socially_appropriate_9' :'etwas sozial unangemessen',
            'q_socially_appropriate_1': 'sehr sozial angemessen'
        })

        yield(pages.SurveyQuestionsAll,  {
            'q_all_other_players': np.random.choice(likert_choices),
            'q_all_communication': 'Ich weiß es nicht.',
            'q_socially_appropriate_10': 'sehr sozial unangemessen',
            'q_socially_appropriate_9' :'etwas sozial unangemessen',
            'q_socially_appropriate_1': 'sehr sozial angemessen'
        })

        yield SubmissionMustFail(pages.SurveyQuestionsFalk, {
            'q_falk1': '-1',
            'q_falk2': '10',
            'q_falk3': np.random.choice(likert_choices),
            'q_falk4': np.random.choice(likert_choices),
            'q_falk5': np.random.choice(likert_choices)
        })

        yield SubmissionMustFail(pages.SurveyQuestionsFalk, {
            'q_falk1': '0',
            'q_falk2': '11',
            'q_falk3': np.random.choice(likert_choices),
            'q_falk4': np.random.choice(likert_choices),
            'q_falk5': np.random.choice(likert_choices)
        })

        yield(pages.SurveyQuestionsFalk, {
            'q_falk1': '0',
            'q_falk2': '10',
            'q_falk3': np.random.choice(likert_choices),
            'q_falk4': np.random.choice(likert_choices),
            'q_falk5': np.random.choice(likert_choices)
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