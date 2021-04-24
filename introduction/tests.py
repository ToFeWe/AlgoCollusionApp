from otree.api import Currency as c, currency_range
from otree.models import group
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail


class PlayerBot(Bot):
    cases = ['all_wrong', 'nothing_wrong', 'some_wrong']

    def play_round(self):
        
        # Treatment indicators for checking the template
        treatment = self.group.group_treatment
        n_players = 2 if treatment  in ['1H1A', '2H0A'] else 3

        # Check if dropout note is shown to the participants at the beginning of the experiment
        assert "Bezahlung und werden von zukünftigen Onlineexperimenten ausgeschlossen" in self.html
        yield(pages.Introduction_1_Welcome)
        
        # Correct show up
        assert "Unabhängig davon erhalten Sie 4" in self.html

        # Correct exchange rate
        assert "Dabei entsprechen 130" in self.html

        # Correct number of consumer
        assert "Alle Firmen bieten 60 Einheiten des vergleichbaren Produktes an." in self.html

        # Check player number specific info
        if n_players == 2:
            assert "jedem Markt verkauft eine weitere Firma" in self.html
            assert "treffen in jeder Runde eines Durchgangs auf dieselbe Firma" in self.html
            assert "beide Firmen Ihre Produkte" in self.html
        else:
            assert "jedem Markt verkaufen zwei weitere Firmen" in self.html
            assert "treffen in jeder Runde eines Durchgangs auf dieselben Firmen" in self.html
            assert "zwei oder alle drei Firmen Ihre Produkte" in self.html


        yield(pages.Introduction_2_Main)
        
        # Check if the correct examples are shown
        if n_players == 2:
            assert "Firma C" not in self.html
        else:
            assert "Firma C" in self.html
        
        yield(pages.Introduction_3_Examples)

        # Check if algo stuff is shown
        if treatment not in ['3H0A', '2H0A']:
            if treatment == '2H1A':
                assert 'entscheiden zwei Teilnehmerinnen und Teilnehmer' in self.html
            elif treatment in ['1H1A', '1H2A']:
                assert 'entscheidet eine Teilnehmerin bzw. ein Teilnehmer selbst' in self.html
            else:
                raise Warning('There is a treatment that I dont know.')


            if treatment == '1H2A':
                assert 'Firma B und C werden in allen Runden mit einem Algorithmus ausgestattet' in self.html
            elif treatment == '1H1A':
                assert 'Firma B wird in allen Runden mit einem Algorithmus ausgestattet' in self.html
            elif treatment == '2H1A':
                assert 'Firma C wird in allen Runden mit einem Algorithmus ausgestattet' in self.html

            # Algo page only shown in the treatments with algorithmen
            yield(pages.Introduction_4_Algos)

        #  Check for player number specific info
        if n_players == 2:
            assert "Durchgang werden sie mit einer/einem anderen Teilnehmer:in" in self.html
        else:
            assert "Durchgang werden sie mit anderen Teilnehmer:innen" in self.html

        # Continuation probability shown
        assert "Die Wahrscheinlichkeit, dass eine weitere Runde gespielt wird, liegt bei 95 %." in self.html
        yield(pages.Introduction_5_Procedure)
        


        # Check if the quiz works properly
        if self.case == 'nothing_wrong':
            yield(pages.Quiz, {
            'q_how_many_customer': 60,
            'q_after_fixed_round': '95%',
            'q_consumer_wtp':4,
            'q_profit_1': 60,
            'q_profit_2': 90 if n_players == 2 else 60
            })
        else:
            # Let the submission fail for three times 
            if self.case == 'some_wrong':
                for tries in range(1,3):
                    # I can submit two times smth wrong
                    yield SubmissionMustFail(pages.Quiz, {
                    'q_how_many_customer': 60,
                    'q_after_fixed_round': '95%',
                    'q_consumer_wtp':4,
                    'q_profit_1': 20,
                    'q_profit_2': 10
                    }, error_fields=['q_profit_1', 'q_profit_2'])

                    # Check if error message is shown
                    assert 'Ihre Antwort war leider nicht korrekt' in self.html

                    # Check if the counters work
                    assert self.player.counter_q_profit_1 == tries, 'Counter did not work'
                    assert self.player.counter_q_profit_2 == tries, 'Counter did not work'
                    assert self.player.counter_how_many_customer == 0, 'Counter did not work'
                # After this it is just accepted what I answered.
                yield(pages.Quiz, {
                'q_how_many_customer': 60,
                'q_after_fixed_round': '95%',
                'q_consumer_wtp':4,
                'q_profit_1': 60,
                'q_profit_2': 90 if n_players == 2 else 60
                })
                # We should not see Answers now given that I answered correctly in the last try

            elif self.case == 'all_wrong':
                # I can submit two times smth wrong
                for tries in range(1,3):
                    yield SubmissionMustFail(pages.Quiz, {
                    'q_how_many_customer': 30,
                    'q_after_fixed_round': '20%',
                    'q_consumer_wtp':2,
                    'q_profit_1': 20,
                    'q_profit_2': 2
                    }, error_fields=['q_how_many_customer',
                                     'q_after_fixed_round',
                                     'q_consumer_wtp',
                                     'q_profit_1',
                                     'q_profit_2'])

                    # Check if error message is shown
                    assert 'Ihre Antwort war leider nicht korrekt' in self.html
                    assert self.player.counter_q_profit_1 == tries, 'Counter did not work'
                    assert self.player.counter_q_profit_2 == tries, 'Counter did not work'
                    assert self.player.counter_consumer_wtp == tries, 'Counter did not work'
                    assert self.player.counter_how_many_customer == tries, 'Counter did not work'
                    assert self.player.counter_after_fixed_round == tries, 'Counter did not work'

                # After this it is just accepted that I fucked up and the answers are shown
                yield (pages.Quiz, {
                'q_how_many_customer': 30,
                'q_after_fixed_round': '20%',
                'q_consumer_wtp':2,
                'q_profit_1': 20,
                'q_profit_2': 2
                })


                # After the submission failed for three times, the page should auto-advance and 
                # the respective explanations should be shown
                assert "Beachten Sie: Sie haben mindestens eine Frage falsch beantwortet." in self.html
                assert "Der Markt hat <b>60 identische Kunden</b>." in self.html
                assert "endet also nach jeder Runde mit einer Wahrscheinlichkeit von 5 %." in self.html
                assert "Jeder Kunde ist bereit maximal <b>4 Taler</b>" in self.html


                assert "1 Taler x 60 Kunden = <b>60 Taler</b>" in self.html
                if n_players == 2:
                    assert "3 Taler x 30 Kunden = <b>90 Taler</b>" in self.html
                else:
                    assert "3 Taler x 20 Kunden = <b>60 Taler</b>" in self.html
                
                yield(pages.Quiz_Results)
