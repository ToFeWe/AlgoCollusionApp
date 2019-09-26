from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    # def after_all_players_arrive(self):
    #     # In the first round for the app group according to shuffle rules
    #     if self.round_number == 1:
    #         self.subsession.do_my_shuffle()
    #     # Then apply this structure to each round for the given app
    #     # Note that this way we have a new matching if we play the app for
    #     # multiple times.
    #     # If we change the constants in each app accordingly.
    #     for subsession in self.subsession.in_rounds(2, Constants.num_rounds):
    #         subsession.group_like_round(1)

    #     # Initialize variable that shows if we still play in the first round 
    #     # of the app
    #     self.session.vars['playing'] = True

    def is_displayed(self):
        return self.round_number == 1

class StartExperiment(Page):
    def is_displayed(self):
        return self.round_number == 1

class NextRound(WaitPage):
    # We wait for all players in the Subsession since we
    # currently write the continuation variable to the session dict
    # TODO: Question is if we want to have group specific continuation
    # TODO: or session specific?
    wait_for_all_groups = True

    def is_displayed(self):
        return self.session.vars['playing']

    def after_all_players_arrive(self):



        # Check if we continue to play
        # Note that the later *self.session.vars['playing']* is there to prevent
        # that we redraw the random number once we already decided to stop
        # self.session.vars['playing'] is initalized to *True* in the session
        # start up 
        if self.round_number > Constants.fixed_rounds and self.session.vars['playing']:
            r_number = random.random()
            if r_number > Constants.cont_prob:
                self.session.vars['playing'] = False
                # Remember which was the last round we played
                self.session.vars['last_round'] = self.round_number - 1
                self.subsession.last_round = self.round_number - 1

                # If we played the last round, set the final payoff for all players in all groups
                for g in self.subsession.get_groups():
                    for p in g.get_players(): 
                        p.set_final_payoff()
            else:
                # If we are still playing, get the recommendation for the current round
                # given that the group is in a treatment with recommendation.
                for current_group in self.subsession.get_groups():
                    p1 = current_group.get_player_by_id(1)
                    treatment =  p1.participant.vars['group_treatment']
                    if treatment == 'recommendation':
                        current_group.get_recommendation(round_number=self.round_number)
        else:
            # If we are still playing, get the recommendation for the current round
            # given that the group is in a treatment with recommendation.
            # TODO: With the new treatment structure we can simplify this
            for current_group in self.subsession.get_groups():
                p1 = current_group.get_player_by_id(1)
                treatment =  p1.participant.vars['group_treatment']
                if treatment == 'recommendation':
                    current_group.get_recommendation(round_number=self.round_number)


class Decide(Page):
    form_model = 'player'
    form_fields = ['price']

    def is_displayed(self):
        return self.session.vars['playing']

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
    def after_all_players_arrive(self):
        self.group.set_profits_round()

    def is_displayed(self):
        return self.session.vars['playing']


class RoundResults(Page):
    def vars_for_template(self):
        treatment =  self.participant.vars['group_treatment']

        opponents = [p for p in self.group.get_players() if p != self.player]
        return {
            'opponents': opponents,
            'treatment': treatment
        }

    def is_displayed(self):
        return self.session.vars['playing']


class HistoryResults(Page):
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

    def is_displayed(self):
        return self.session.vars['playing']

class LastFixedRound(Page):
    def is_displayed(self):
        return self.round_number == Constants.fixed_rounds

    def vars_for_template(self):
        return {'fixed_rounds': 
                Constants.fixed_rounds}



page_sequence = [
    ShuffleWaitPage,
    NextRound,
    StartExperiment,
    Decide,
    RoundWaitPage,
    RoundResults,
    HistoryResults,
    LastFixedRound
]
