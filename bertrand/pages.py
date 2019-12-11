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
    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def after_all_players_arrive(self):
        # Get the recommendation for the current round
        # given that the group is in a treatment with recommendation.
        p1 = self.group.get_player_by_id(1)
        treatment =  p1.participant.vars['group_treatment']

        # In the baseline treatment there is no recommendation,
        # but else always.
        if treatment != 'baseline':
            self.group.get_recommendation(round_number=self.round_number,
                                          treatment=treatment)


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
        label_decide = "Bitte wählen sie Ihren Preis zwischen {} und {} Taler:".format(Constants.deviation_price,
                                                                                 Constants.monopoly_price)
        return {
            "label_decide": label_decide,
            'exchange_rate': int(1 / self.session.config['real_world_currency_per_point']), # To avoid comma
            'treatment': treatment,
            'player_price_last_round': player_price_last_round,
            'super_game_count': self.subsession.this_app_constants()['super_game_count']
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
            'treatment': treatment,
            'super_game_count': self.subsession.this_app_constants()['super_game_count']
        }


class EndSG(Page):

    def is_displayed(self):
        # Only displayed in the last round, e.g. the number of rounds is equal 
        # to the random raw of round numbers from before
        return self.round_number == self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        # Set the final payoff for player for the given Super Game
        # Nothing random here, hence we can execute it in vars_for_template
        self.player.set_final_payoff()

        return {
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee'],
            'final_payoff_euro' : float(self.participant.payoff_plus_participation_fee()),
            'payoff_coins': self.participant.payoff,
            'super_game_count': self.subsession.this_app_constants()['super_game_count'],
            'accumulated_profit': self.player.accumulated_profit
        }

        


page_sequence = [
    StartExperiment,
    NextRound,
    Decide,
    RoundWaitPage,
    RoundResults,
    EndSG
]
