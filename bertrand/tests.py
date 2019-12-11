from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail

import random

def check_player_groups(player_id, group_id, super_game):
    """Helper function to check if the matching works for
    a subset of users.
    
    """
    if player_id == 1:
        return group_id == 1
    elif player_id == 4:
        return group_id == 2
    elif player_id == 7:
        return group_id == 3
    elif player_id == 10:
        return group_id == 4
    elif player_id == 13:
        return group_id == 5
    elif player_id == 16:
        return group_id == 6
    elif player_id == 19:
        return group_id == 7
    elif player_id == 22:
        return group_id == 8
    elif player_id == 25:
        return group_id == 9
    elif player_id == 28:
        return group_id == 10
    elif player_id == 31:
        return group_id == 11
    elif player_id == 34:
        return group_id == 12

    # Test  some players for which the group if changes
    elif player_id == 8:
        if super_game == 1:
            return group_id == 3
        elif super_game == 2:
            return group_id == 2
        elif super_game == 3:
            return group_id == 1
        else:
            return False # Must be an error then
    elif player_id == 12:
        if super_game == 1:
            return group_id == 4
        elif super_game == 2:
            return group_id == 5
        elif super_game == 3:
            return group_id == 6
        else:
            return False # Must be an error then
    elif player_id == 21:
        if super_game == 1:
            return group_id == 7
        elif super_game == 2:
            return group_id == 8
        elif super_game == 3:
            return group_id == 9
        else:
            return False # Must be an error then
    elif player_id == 20:
        if super_game == 1:
            return group_id == 7
        elif super_game == 2:
            return group_id == 9
        elif super_game == 3:
            return group_id == 8
        else:
            return False # Must be an error then

    elif player_id == 30:
        if super_game == 1:
            return group_id == 10
        elif super_game == 2:
            return group_id == 11
        elif super_game == 3:
            return group_id == 12
        else:
            return False # Must be an error then
    
    elif player_id == 35:
        if super_game == 1:
            return group_id == 12
        elif super_game == 2:
            return group_id == 11
        elif super_game == 3:
            return group_id == 10
        else:
            return False # Must be an error then

    else:
        # If its none of the players we want to test
        # we return True.
        return True


def check_others_in_group(other_group_members, player_id, super_game):
    """ Helper function to check if the other group members are correct.
    """
    ids_other_members = [group_member.participant.id_in_session for group_member in other_group_members]
    
    if player_id == 1:
        if super_game == 1:
            return all([2 in ids_other_members, 
                        3 in ids_other_members])
        elif super_game == 2:
            return all([5 in ids_other_members, 
                        9 in ids_other_members])
        elif super_game == 3:
            return all([6 in ids_other_members, 
                        8 in ids_other_members])
        else:
            return False # Must be an error else
    elif player_id == 5:
        if super_game == 1:
            return all([4 in ids_other_members, 
                        6 in ids_other_members])
        elif super_game == 2:
            return all([1 in ids_other_members, 
                        9 in ids_other_members])
        elif super_game == 3:
            return all([7 in ids_other_members, 
                        3 in ids_other_members])
        else:
            return False # Must be an error else
    elif player_id == 15:
        if super_game == 1:
            return all([13 in ids_other_members, 
                        14 in ids_other_members])
        elif super_game == 2:
            return all([11 in ids_other_members, 
                        16 in ids_other_members])
        elif super_game == 3:
            return all([10 in ids_other_members, 
                        17 in ids_other_members])
        else:
            return False # Must be an error else

    elif player_id == 27:
        if super_game == 1:
            return all([25 in ids_other_members, 
                        26 in ids_other_members])
        elif super_game == 2:
            return all([19 in ids_other_members, 
                        23 in ids_other_members])
        elif super_game == 3:
            return all([22 in ids_other_members, 
                        20 in ids_other_members])
        else:
            return False # Must be an error else

    elif player_id == 31:
        if super_game == 1:
            return all([32 in ids_other_members, 
                        33 in ids_other_members])
        elif super_game == 2:
            return all([35 in ids_other_members, 
                        30 in ids_other_members])
        elif super_game == 3:
            return all([36 in ids_other_members, 
                        29 in ids_other_members])
        else:
            return False # Must be an error else

    elif player_id == 36:
        if super_game == 1:
            return all([35 in ids_other_members, 
                        34 in ids_other_members])
        elif super_game == 2:
            return all([28 in ids_other_members, 
                        32 in ids_other_members])
        elif super_game == 3:
            return all([31 in ids_other_members, 
                        29 in ids_other_members])
        else:
            return False # Must be an error else


    else:
        # If we do not check the player we return
        # True by default.
        return True         
          
class SharedPlayerBot(Bot):
    cases = ['random_price']
    #, 'simple', 
    # , 'hip_hop_player', 'deviation'
    def play_round(self):
        case = self.case
        if case == 'simple':
            if self.round_number == 1:
                yield(pages.StartExperiment)
                
                # Check the group matching for some arbitrary players conditional
                # on the super game.
                assert check_player_groups(player_id = self.participant.id_in_session,
                                           group_id = self.group.id_in_subsession,
                                           super_game = self.subsession.this_app_constants()['super_game_count']), 'Group matching Error for player {} in super game {}'.format(self.participant.id_in_session,
                                                                                                                                                                                self.subsession.this_app_constants()['super_game_count'])
                assert check_others_in_group(other_group_members = self.player.get_others_in_group(),
                                             player_id = self.participant.id_in_session,
                                             super_game = self.subsession.this_app_constants()['super_game_count']), 'Other group member error for player {} in super game {}'.format(self.participant.id_in_session,
                                                                                                                                                                                      self.subsession.this_app_constants()['super_game_count'])

            if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:

                # Check if the recommendation works properly for all rounds except the first
                if self.session.config['group_treatment'] != 'baseline' and self.round_number >1:
                    group_last_round = self.group.in_previous_rounds()[-1]
                    prices_last_round = [p.price for p in group_last_round.get_players()]
                    n_unique_prices = len(set(prices_last_round))
                    
                    # If there were more than one price, there must have been a deviation
                    if n_unique_prices != 1:
                        assert "In der vergangenen Runde gab es Abweichungen vom empfohlenen Preis" in self.html
                        if self.session.config['group_treatment'] == 'recommendation_simple':
                            assert "einen Preis von <b>1 Taler.</b>" in self.html
                            assert self.group.recommendation == 1
                        elif self.session.config['group_treatment'] == 'recommendation_lowest_price':
                            min_price = min(prices_last_round)
                            assert "einen Preis von <b>{} Taler.</b>".format(int(min_price)) in self.html
                            assert self.group.recommendation == min_price

                    else:
                        assert self.group.recommendation == 10
                        assert "vergangenen Runde haben alle Firmen einen Preis" in self.html
                        if list(set(prices_last_round))[0] != 10:
                            assert "Für einen höheren Gesamtgewinn empfiehlt" in self.html
                        else:
                            assert "<b>10 Taler</b> beizubehalten" in self.html

                yield(pages.Decide, {'price': 10})

                # Everyone plays the same price here,
                # Hence, everyone must be a winner.
                assert self.player.is_winner, "The player is not a winner even though everyone played the same price"

                yield(pages.RoundResults)

            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
                round_number_draw = self.subsession.this_app_constants()['round_number_draw']
                # Each round everyone plays a price of 10. Hence, the market is shared for each round
                # across all rounds.
                accumulated_payoff_in_app = round_number_draw * 10 * Constants.m_consumer / Constants.players_per_group
                assert str(int(accumulated_payoff_in_app)) in self.html, "Not there"

                sg_counter = self.subsession.this_app_constants()['super_game_count']
                key_name = "final_payoff_sg_" + str(sg_counter)        
                assert accumulated_payoff_in_app == self.participant.vars[key_name]
                
                assert "insgesamt einen Gewinn von <b>{} Taler".format(int(accumulated_payoff_in_app)) in self.html
                if sg_counter == 1 or sg_counter == 2:
                    assert "Sie spielen jetzt das gleiche Spiel erneut" in self.html
                else:
                    assert "Dies war das letzte Spiel" in self.html
                assert "dies die letzte Runde des {}. Spiels".format(self.subsession.this_app_constants()['super_game_count']) in self.html
                yield(pages.EndSG)


        if case == 'random_price':
            if self.round_number == 1:
                yield(pages.StartExperiment)

                # Check the group matching for some arbitrary players conditional
                # on the super game.
                assert check_player_groups(player_id = self.participant.id_in_session,
                                           group_id = self.group.id_in_subsession,
                                           super_game = self.subsession.this_app_constants()['super_game_count']), 'Group matching Error for player {} in super game {}'.format(self.participant.id_in_session,
                                                                                                                                                                                self.subsession.this_app_constants()['super_game_count'])
                assert check_others_in_group(other_group_members = self.player.get_others_in_group(),
                                             player_id = self.participant.id_in_session,
                                             super_game = self.subsession.this_app_constants()['super_game_count']), 'Other group member error for player {} in super game {}'.format(self.participant.id_in_session,
                                                                                                                                                                                      self.subsession.this_app_constants()['super_game_count'])
                if self.session.config['group_treatment'] != 'baseline':
                    assert 'einen Preis von <b>10 Taler.</b>' in self.html

            if self.round_number <= self.subsession.this_app_constants()['round_number_draw']:
                # Check if the recommendation works properly for all rounds except the first
                if self.session.config['group_treatment'] != 'baseline' and self.round_number >1:
                    group_last_round = self.group.in_previous_rounds()[-1]
                    prices_last_round = [p.price for p in group_last_round.get_players()]
                    n_unique_prices = len(set(prices_last_round))

                    # If there were more than one price, there must have been a deviation
                    if n_unique_prices != 1:
                        if self.session.config['group_treatment'] == 'recommendation_simple':
                            assert "einen Preis von <b>1 Taler.</b>" in self.html
                            assert self.group.recommendation == 1
                        elif self.session.config['group_treatment'] == 'recommendation_lowest_price':
                            min_price = min(prices_last_round)
                            assert "einen Preis von <b>{} Taler.</b>".format(int(min_price)) in self.html
                            assert self.group.recommendation == min_price
                    else:
                        assert self.group.recommendation == 10
                        assert "vergangenen Runde haben alle Firmen einen Preis" in self.html
                        if list(set(prices_last_round))[0] != 10:
                            assert "Für einen höheren Gesamtgewinn empfiehlt" in self.html
                        else:
                            assert "<b>10 Taler</b> beizubehalten" in self.html
                
                # Check in the first round if the price bounds are correct
                if self.round_number == 1:
                    yield SubmissionMustFail(pages.Decide, {'price': 0}, error_fields=['price'])
                    yield SubmissionMustFail(pages.Decide, {'price': 11}, error_fields=['price']) 
                    yield SubmissionMustFail(pages.Decide, {'price': 1.1}, error_fields=['price']) 
                # Check recommendation part
                if self.session.config['group_treatment'] != 'baseline':
                    assert "allen Firmen" in self.html
                yield(pages.Decide, {'price': random.randint(1,10)})
                

                assert str(int(self.player.price)) in self.html
                assert str(int(self.group.winning_price)) in self.html
                if self.player.price == self.group.winning_price:
                    assert self.player.is_winner, "The player is not a winner even though everyone played the minimal price"
                    assert str(int(self.group.winning_price/self.group.n_winners * Constants.m_consumer)) in self.html
                else:
                    assert not self.player.is_winner
                
                yield(pages.RoundResults)

            if self.round_number == self.subsession.this_app_constants()['round_number_draw']:
                round_number_draw = self.subsession.this_app_constants()['round_number_draw']

                accumulated_payoff_in_app = sum([p_in_r.profit for p_in_r in self.player.in_all_rounds()])
                assert str(int(accumulated_payoff_in_app)) in self.html, "Not there"

                sg_counter = self.subsession.this_app_constants()['super_game_count']
                key_name = "final_payoff_sg_" + str(sg_counter)        
                assert accumulated_payoff_in_app == self.participant.vars[key_name]

                assert "insgesamt einen Gewinn von <b>{} Taler".format(int(accumulated_payoff_in_app)) in self.html
                if sg_counter == 1 or sg_counter == 2:
                    assert "Sie spielen jetzt das gleiche Spiel erneut" in self.html
                else:
                    assert "Dies war das letzte Spiel" in self.html
                assert "dies die letzte Runde des {}. Spiels".format(self.subsession.this_app_constants()['super_game_count']) in self.html
                yield(pages.EndSG)


class PlayerBot(SharedPlayerBot):
    pass  