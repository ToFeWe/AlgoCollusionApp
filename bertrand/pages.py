from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random

class StartExperiment(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):
        return {
            'super_game_count': self.subsession.this_app_constants()['super_game_count']
        }

class NextRound(WaitPage):
    wait_for_all_groups = True
    
    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def after_all_players_arrive(self):
        # Get the recommendation for the current round
        # given that the group is in a treatment with recommendation.
        for current_group in self.subsession.get_groups():
            p1 = current_group.get_player_by_id(1)
            treatment =  p1.participant.vars['group_treatment']
            if treatment == 'recommendation':
                current_group.get_recommendation(round_number=self.round_number)



class Decide(Page):
    form_model = 'player'
    form_fields = ['price']

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        treatment =  self.participant.vars['group_treatment']

        # In the first round there is no last price
        # We set it here to -1, as it won't be displayed anyways,
        # given the fixed recommendation in the first period.
        if self.round_number == 1:
            player_price_last_round = -1
        else:
            player_price_last_round = self.player.in_previous_rounds()[-1].price
        label_decide = "Bitte wählen sie Ihren Preis zwischen {} und {} Talern:".format(Constants.deviation_price,
                                                                                 Constants.monopoly_price)
        return {
            "label_decide": label_decide,
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'treatment': treatment,
            'player_price_last_round': player_price_last_round
            }


class RoundWaitPage(WaitPage):

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def after_all_players_arrive(self):
        self.group.set_profits_round()

class RoundResults(Page):

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        treatment =  self.participant.vars['group_treatment']

        opponents = [p for p in self.group.get_players() if p != self.player]
        return {
            'opponents': opponents,
            'treatment': treatment
        }


class HistoryResults(Page):

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        opponents = [p for p in self.group.get_players() if p != self.player]
        # ids_opponents = [p.id_in_group for p in opponents]
        player_1 = self.group.get_player_by_id(1)
        player_2 = self.group.get_player_by_id(2)
        player_3 = self.group.get_player_by_id(3)

        prices_player_1 = [p.price for p in player_1.in_all_rounds()]
        prices_player_2 = [p.price for p in player_2.in_all_rounds()]
        prices_player_3 = [p.price for p in player_3.in_all_rounds()]

        treatment =  self.participant.vars['group_treatment']
        round_list = list(range(1, self.round_number + 1))

        # Note that past_recommendation is simply an empty list for the baseline treatment
        # but it is not used anyways.
        past_recommendations = [g.recommendation for g in self.group.in_all_rounds()]

        out_dict = {
        'prices_player_1': prices_player_1,
        'prices_player_2': prices_player_2,
        'prices_player_3': prices_player_3,
        'treatment': treatment,
        'past_recommendations': past_recommendations,
        'round_list': round_list
        }

        # TODO: For simplicity hardcoded
        return out_dict


class EndRound(Page):

    def is_displayed(self):
        # Only displayed in the last round, e.g. the number of rounds is equal #
        # to the random raw of round numbers from before
        return self.round_number == self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        # Set the final payoff for all players in all groups for the given Super Game
        for g in self.subsession.get_groups():
            for p in g.get_players(): 
                p.set_final_payoff()

        return {
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee'],
            'final_payoff_euro' : float(self.participant.payoff_plus_participation_fee()),
            'payoff_coins': self.participant.payoff,
            'super_game_count': self.subsession.this_app_constants()['super_game_count'],
            'accumulated_profit': self.player.accumulated_profit
        }

        


page_sequence = [
    NextRound,
    StartExperiment,
    Decide,
    RoundWaitPage,
    RoundResults,
    HistoryResults,
    EndRound
]
