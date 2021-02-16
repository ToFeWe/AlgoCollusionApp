from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class StartExperiment(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()
        template_vars = {
            'super_game_count': self.subsession.this_app_constants()['super_game_count'],
            'player_id': Constants.firma_id_map[self.player.id_in_group]
        }
        template_vars.update(additional_template_vars)
        return template_vars

class Decide(Page):
    form_model = 'player'
    form_fields = ['price']

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()
        label_decide = "Bitte wählen sie Ihren Preis zwischen {} und {} Talern:".format(Constants.lowest_price,
                                                                                        Constants.maximum_price)
        template_vars = {
            "label_decide": label_decide,
            'exchange_rate': int(1 / self.session.config['real_world_currency_per_point']), # To avoid comma
            'super_game_count': self.subsession.this_app_constants()['super_game_count']
            }
        template_vars.update(additional_template_vars)
        return template_vars

    def before_next_page(self):
        # Algorithm also decides on its price if there is any
        # Note that we use the prices from the last period here in
        # the function and not from this round!
        if self.group.group_treatment not in ['3H0A', '2H0A']:
            self.group.set_algo_price()

class RoundWaitPage(WaitPage):

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def after_all_players_arrive(self):
        # Set the profits for the round
        self.group.calc_round_profit()

class RoundResults(Page):

    def is_displayed(self):
        # Only displayed if we still play, e.g. the number of rounds is equal or
        # below the random raw of round numbers from before
        return self.round_number <= self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        additional_template_vars = self.group.get_additional_template_variables()
        player_letter, opponent_letters, opponent_prices = self.player.get_market_infos()
        template_vars = {
            'opponents_prices': opponent_prices,
            'opponent_letters': opponent_letters,
            'player_letter': player_letter,
            'super_game_count': self.subsession.this_app_constants()['super_game_count']
        }
        template_vars.update(additional_template_vars)
        return template_vars


class EndSG(Page):

    def is_displayed(self):
        # Only displayed in the last round, e.g. the number of rounds is equal 
        # to the random raw of round numbers from before
        return self.round_number == self.subsession.this_app_constants()['round_number_draw']

    def vars_for_template(self):
        # Set the final payoff for player for the given Super Game
        # Nothing random here, hence we can execute it in vars_for_template
        self.player.set_final_payoff()

        # Template variables
        additional_template_vars = self.group.get_additional_template_variables()
        template_vars = {
            'final_payoff_euro' : float(self.participant.payoff_plus_participation_fee()),
            'payoff_coins': self.participant.payoff,
            'super_game_count': self.subsession.this_app_constants()['super_game_count'],
            'accumulated_profit': self.player.accumulated_profit
        }
        template_vars.update(additional_template_vars)
        return template_vars

        


page_sequence = [
    StartExperiment,
    Decide,
    RoundWaitPage,
    RoundResults,
    EndSG
]
