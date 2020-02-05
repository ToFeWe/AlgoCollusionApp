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

        if self.session.config['group_treatment'] !='baseline':
            yield SubmissionMustFail(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '-1',
               'q_alg_no_recommendation': '11',
               'q_alg_relevant_other_player': '-1',
               'q_alg_comments': 'lala',
               'q_agree_statement_1': '-1',
               'q_agree_statement_2': '11',
               'q_agree_statement_3': '11',
               'q_agree_statement_4': '-1'
            },
            error_fields=['q_alg_helpful', 'q_alg_no_recommendation',
                          'q_alg_relevant_other_player', 'q_agree_statement_1',
                          'q_agree_statement_2', 'q_agree_statement_3',
                          'q_agree_statement_4'])

            yield SubmissionMustFail(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '',
               'q_alg_no_recommendation': '-1',
               'q_alg_relevant_other_player': '22',
               'q_alg_comments': 'lala',
               'q_agree_statement_1': '11',
               'q_agree_statement_2': '-1',
               'q_agree_statement_3': '-1',
               'q_agree_statement_4': '11'
            },
            error_fields=['q_alg_helpful', 'q_alg_no_recommendation',
                          'q_alg_relevant_other_player', 'q_agree_statement_1',
                          'q_agree_statement_2', 'q_agree_statement_3',
                          'q_agree_statement_4'])

            yield(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '0',
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '10',
               'q_alg_comments': 'lala',
               'q_agree_statement_1': np.random.choice(likert_choices),
               'q_agree_statement_2': np.random.choice(likert_choices),
               'q_agree_statement_3': '0',
               'q_agree_statement_4': '10'

            })

        yield SubmissionMustFail(pages.SurveyQuestionsFalk, {
            'q_falk1': '-1',
            'q_falk2': '22',
            'q_falk3': '11',
            'q_falk4': '',
            'q_falk5': 'YOLO',
            'q_falk6': ''
        }, error_fields=['q_falk1', 'q_falk2', 'q_falk3',
                         'q_falk4', 'q_falk5', 'q_falk6'
        ])

        yield(pages.SurveyQuestionsFalk, {
            'q_falk1': '0',
            'q_falk2': '10',
            'q_falk3': np.random.choice(likert_choices),
            'q_falk4': np.random.choice(likert_choices),
            'q_falk5': np.random.choice(likert_choices),
            'q_falk6': np.random.choice(likert_choices)
        })

        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 15,
            'q_gender': 'qq',
            'q_study_level': '',
            'q_study_field': 'Econ', 
            'q_semester': -1,
            'q_abitur': 0.0,
            'q_math': 6.1,
            'q_budget': -1,
            'q_spending': 1000001,
            'q_n_experiment': -1,
            'q_similar_experiment': '',
            'q_other_notes': 'lalala'

        }, error_fields=['q_age', 'q_gender', 'q_study_level',
        'q_abitur', 'q_math', 'q_budget', 
        'q_spending', 'q_n_experiment', 'q_similar_experiment'])

        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 100,
            'q_gender': 'Nein',
            'q_study_level': '22',
            'q_study_field': 'Wiwi', 
            'q_semester': 99,
            'q_abitur': 6.001,
            'q_math': 0.999,
            'q_budget': 10000000,
            'q_spending': -9,
            'q_n_experiment': 9999,
            'q_similar_experiment': '',
            'q_other_notes': 'lalala'

        }, error_fields=['q_age', 'q_gender', 'q_study_level',
        'q_abitur', 'q_math', 'q_budget', 
        'q_spending', 'q_n_experiment', 'q_similar_experiment'])

        yield(pages.GeneralQuestions, {
            'q_age': 22,
            'q_gender': 'Männlich',
            'q_study_level': 'Bachelorabschluss',
            'q_study_field': 'Wiwi', 
            'q_semester': 3,
            'q_abitur': 6.0,
            'q_math': 1.0,
            'q_budget': 100,
            'q_spending': 90,
            'q_n_experiment': 4,
            'q_similar_experiment': 'Ja.',
            'q_other_notes': 'lulu'
        })