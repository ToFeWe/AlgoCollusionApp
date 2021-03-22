from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Tobias Werner'

doc = """ An App for a price recommendation system in a market experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):


    def creating_session(self):
        
        for p in self.get_players():
            # For every player another super game is paid
            p.paid_sg = random.choice([1,2,3])
            p.participant.vars['paid_sg'] = p.paid_sg

            # init vars for admin report 
            p.participant.vars['final_money_with_show_up'] = 0
            p.participant.vars['final_money_no_show_up'] = 0

    def vars_for_admin_report(self):
        participants = self.session.get_participants()
        total_payoff_all = sum([p.payoff.to_real_world_currency(self.session) for p in participants])
        mean_payoff_all = total_payoff_all/self.session.num_participants
        return {
            'participants': participants,
            'total_payoff_all': total_payoff_all,
            'mean_payoff_all': mean_payoff_all,
            'participation_fee': self.session.config['participation_fee'],
        }
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Indicator which super game is paid
    paid_sg = models.IntegerField()
        