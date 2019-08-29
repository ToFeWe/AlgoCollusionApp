from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class Introduction_1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction_2(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction_3(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction_4(Page):
    def is_displayed(self):
        return self.round_number == 1

class Algorithm_Introduction(Page):
    def is_displayed(self):
        treatment =  self.participant.vars['group_treatment']
        return treatment == 'recommendation' and self.round_number == 1



 


class Quiz(Page):
    form_model = 'player'

    def get_form_fields(self):
        treatment =  self.participant.vars['group_treatment']
        if treatment == 'baseline':
            return ['q_how_many_customer',
                    'q_after_fixed_round',
                    'q_profit_1',
                    'q_profit_2',
                    'q_profit_3']
        else:
            return ['q_how_many_customer',
                    'q_after_fixed_round',
                    'q_profit_1',
                    'q_profit_2',
                    'q_profit_3',
                    'q_goal_alg']
    
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        # Group treatment stored in participant.vars of
        # first group member.
        treatment =  self.participant.vars['group_treatment']
        
        return {
            'treatment': treatment
        }

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

        label_decide = "Bitte wählen sie Ihren Preis zwischen {} und {} Talern:".format(Constants.deviation_price,
                                                                                 Constants.monopoly_price)
        return {
            "label_decide": label_decide,
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'treatment': treatment
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
    Introduction_1,
    Introduction_2,
    Introduction_3,
    Introduction_4,
    Algorithm_Introduction,
    Quiz,
    NextRound,
    StartExperiment,
    Decide,
    RoundWaitPage,
    RoundResults,
    HistoryResults,
    LastFixedRound
]
