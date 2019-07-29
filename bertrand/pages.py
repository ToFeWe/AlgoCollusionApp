from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Decide(Page):
    form_model = 'player'
    form_fields = ['price']


class RoundWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs_round()


class RoundResults(Page):
    def vars_for_template(self):
        opponents = [p for p in self.group.get_players() if p != self.player]
        return {
            'opponents': opponents
        }

class HistoryResults(Page):
    def vars_for_template(self):
        opponents = [p for p in self.group.get_players() if p != self.player]
        #ids_opponents = [p.id_in_group for p in opponents]
        player_1 = self.group.get_player_by_id(1)
        player_2 = self.group.get_player_by_id(2)
        player_3 = self.group.get_player_by_id(3)

        prices_player_1 = [p.price for p in player_1.in_all_rounds()]
        prices_player_2 = [p.price for p in player_2.in_all_rounds()]
        prices_player_3 = [p.price for p in player_3.in_all_rounds()]
        round_list = list(range(1,self.round_number+1))



        # TODO: For simplicity hardcoded 
        return {    
            'prices_player_1': prices_player_1,
            'prices_player_2': prices_player_2,
            'prices_player_3': prices_player_3,
            'round_list': round_list
        }

# class EndRoundWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         self.group.set_payoffs_round()

class NextRound(Page):
    pass

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Introduction,
    Decide,
    RoundWaitPage,
    RoundResults,
    HistoryResults,
    NextRound,
    FinalResults
]
