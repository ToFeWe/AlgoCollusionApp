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
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '10',
               'q_alg_comments': 'lala',
               'q_alg_improve': 'testets'
            },
            error_fields=['q_alg_helpful'])

            yield SubmissionMustFail(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '0',
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '11',
               'q_alg_comments': 'lala',
               'q_alg_improve': 'testets'
            }, error_fields=['q_alg_relevant_other_player'])
            yield(pages.SurveyQuestionsAlg, {
               'q_alg_helpful': '0',
               'q_alg_no_recommendation': np.random.choice(likert_choices),
               'q_alg_relevant_other_player': '10',
               'q_alg_comments': 'lala',
               'q_alg_improve': 'testets'
            })
        yield SubmissionMustFail(pages.SurveyQuestionsFalk, {
            'q_falk1': '-1',
            'q_falk2': '10',
            'q_falk3': np.random.choice(likert_choices),
            'q_falk4': np.random.choice(likert_choices),
            'q_falk5': np.random.choice(likert_choices)
        }, error_fields=['q_falk1'])

        yield SubmissionMustFail(pages.SurveyQuestionsFalk, {
            'q_falk1': '0',
            'q_falk2': '11',
            'q_falk3': np.random.choice(likert_choices),
            'q_falk4': np.random.choice(likert_choices),
            'q_falk5': np.random.choice(likert_choices)
        }, error_fields=['q_falk2'])

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
            'q_study_level': 'Weiterführende Schule nicht beendet',
            'q_student': 'Ja',
            'q_study_field': 'Econ',  
            'q_semester': 12,
            'q_n_experiment': 4,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'

        }, error_fields=['q_age'])
        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 16,
            'q_gender': 'Divers',
            'q_study_level': 'nicht beendet',
            'q_study_field': 'Econ',  
            'q_semester': 10,
            'q_student': 'Ja',
            'q_n_experiment': 4,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'

        }, error_fields=['q_study_level'])
        yield SubmissionMustFail(pages.GeneralQuestions, {
            'q_age': 30,
            'q_gender': 'Divers',
            'q_study_level': 'Masterabschluss',
            'q_study_field': 'Econ', 
            'q_student': 'Ja',
            'q_semester': 1,
            'q_n_experiment': -1,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'

        }, error_fields=['q_n_experiment'])

        yield(pages.GeneralQuestions, {
            'q_age': 16,
            'q_gender': 'Divers',
            'q_study_level': 'Masterabschluss',
            'q_study_field': 'Econ',
            'q_student': 'Ja', 
            'q_semester': 12,
            'q_n_experiment': 4,
            'q_similar_experiment': 'Nein.',
            'q_other_notes': 'lalala'
        })