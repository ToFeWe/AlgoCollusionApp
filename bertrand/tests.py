from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

import random

class SharedPlayerBot(Bot):
    cases = ['simple', 'random_price']
    # , 'hip_hop_player', 'deviation'
    def play_round(self):
        case = self.case
        if case == 'simple':
            if self.round_number == 1:
                yield(pages.StartExperiment)
            if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:
                yield(pages.Decide, {'price': 10})

                # Everyone plays the same price here,
                # Hence, everyone must be a winner.
                assert self.player.is_winner, "The player is not a winner even though everyone played the same price"
                assert 'Da Sie den günstigsten Preis gewählt haben' in self.html
                yield(pages.RoundResults)
                yield(pages.HistoryResults)

            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
                round_number_draw = self.subsession.this_app_constants()['round_number_draw']
                assert round_number_draw in [1,2,3]
                # Each round everyone plays a price of 10. Hence, the market is shared for each round
                # across all rounds.
                accumulated_payoff_in_app = round_number_draw * 10 * Constants.m_consumer / Constants.players_per_group
                assert str(int(accumulated_payoff_in_app)) in self.html, "Not there"

                sg_counter = self.subsession.this_app_constants()['super_game_count']
                key_name = "final_payoff_sg_" + str(sg_counter)        
                assert accumulated_payoff_in_app == self.participant.vars[key_name]
                # TODO: Mit richtiger Umrechnungsrate in Euro testen
                yield(pages.EndRound)


        if case == 'random_price':
            if self.round_number == 1:
                yield(pages.StartExperiment)
            if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:
                yield(pages.Decide, {'price': random.randint(1,10)})

                if self.player.price == self.group.winning_price:
                    assert self.player.is_winner, "The player is not a winner even though everyone played the minimal price"
                    assert str(int(self.group.winning_price/self.group.n_winners * Constants.m_consumer)) in self.html
                else:
                    assert not self.player.is_winner
                    assert "ihr Produkt nicht verkauft" in self.html
                yield(pages.RoundResults)
                yield(pages.HistoryResults)

            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
                round_number_draw = self.subsession.this_app_constants()['round_number_draw']

                accumulated_payoff_in_app = sum([p_in_r.profit for p_in_r in self.player.in_all_rounds()])
                assert str(int(accumulated_payoff_in_app)) in self.html, "Not there"

                sg_counter = self.subsession.this_app_constants()['super_game_count']
                key_name = "final_payoff_sg_" + str(sg_counter)        
                assert accumulated_payoff_in_app == self.participant.vars[key_name]
                # TODO: Mit richtiger Umrechnungsrate in Euro testen
                yield(pages.EndRound)


class PlayerBot(SharedPlayerBot):
    pass  