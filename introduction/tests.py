from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail


class PlayerBot(Bot):
    # TODO: rework
    def play_round(self):
        yield(pages.Introduction_1)
        
        # correct show up
        assert "Unabhängig davon erhalten Sie 4" in self.html
        # correct exchange rate
        assert "Dabei entsprechen 100" in self.html
        # correct rounding
        assert "gerundet werden Teilnehmer A 4,7" in self.html

        yield(pages.Introduction_2)

        # Correct deviation price
        assert "einen Preis von 1" in self.html

        # Correct number of consumers
        assert "Der Markt hat 30" in self.html

        # Correct max price
        assert "Jeder Kunde ist bereit bis zu 10" in self.html
        assert "virtuellen Produktmarkt" in self.html
        yield(pages.Introduction_3)
        if self.session.config['group_treatment'] !='baseline':
            assert "erhalten dieselbe Preisempfehlung" in self.html
            yield(pages.Algorithm_Introduction)
            # Intro 4 after Algo
            yield(pages.Introduction_4)

            yield SubmissionMustFail(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '95%',
                'q_profit_1': 61,
                'q_profit_2': 80,
                'q_profit_3': 6.5,
                'q_goal_alg': 'Gesamtgewinne über alle Runden hinweg für alle Firmen zu maximieren.'
            },
                error_fields=['q_profit_1']
            )
            assert self.player.counter_q_profit_1 == 1, 'Counter did not work'
            assert self.player.counter_q_profit_2 == 0, 'Counter did not work'
            assert 'Ihre Antwort war leider nicht korrekt' in self.html

            yield SubmissionMustFail(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '95%',
                'q_profit_1': 60,
                'q_profit_2': 80,
                'q_profit_3': 6.5,
				'q_goal_alg': 'Gesamtgewinne über alle Runden hinweg für einzelne Firmen zu maximieren.'
            },
            error_fields=['q_goal_alg']
            )
            # Has to be zero given submission failed as we did answer nothing 
            assert self.player.counter_goal_alg == 1, 'Counter did not work'
            
            yield SubmissionMustFail(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '95%',
                'q_profit_1': 60,
                'q_profit_2': 80,
                'q_profit_3': 6.5,
                'q_goal_alg': 'Gewinne für einzelne Firmen in einer einzelnen Runde zu maximieren.'

            },
            error_fields=['q_goal_alg']
            )
            # Has to be one given submission failed as we did answer smth wrong 
            assert self.player.counter_goal_alg == 2, 'Counter did not work'


            yield(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '95%',
                'q_profit_1': 60,
                'q_profit_2': 80,
                'q_profit_3': 6.5,
                'q_goal_alg': 'Gesamtgewinne über alle Runden hinweg für alle Firmen zu maximieren.'
            })
        else:
            yield(pages.Introduction_4)
            yield SubmissionMustFail(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '5%',
                'q_profit_1': 60,
                'q_profit_2': 80,
                'q_profit_3': 6.5
            },
            error_fields=['q_after_fixed_round']
            )
            
            assert self.player.counter_q_profit_1 == 0, 'Counter did not work'
            assert self.player.counter_after_fixed_round == 1, 'Counter did not work'
            assert 'Ihre Antwort war leider nicht korrekt' in self.html

            yield SubmissionMustFail(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '5%',
                'q_profit_1': 60,
                'q_profit_2': 81,
                'q_profit_3': 6.5
            },
            error_fields=['q_after_fixed_round', 'q_profit_2']
            )
            
            assert self.player.counter_q_profit_1 == 0, 'Counter did not work'
            assert self.player.counter_after_fixed_round == 2, 'Counter did not work'
            assert self.player.counter_q_profit_2 == 1, 'Counter did not work'

            assert 'Ihre Antwort war leider nicht korrekt' in self.html

            yield(pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '95%',
                'q_profit_1': 60,
                'q_profit_2': 80,
                'q_profit_3': 6.5
            })
