from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math
import itertools

doc = """
Price Recommender Game with Bertrand
"""

class Constants(BaseConstants):
    players_per_group = 3
    name_in_url = 'bertrand'


    # Note that *num_rounds* is used to have an upper bound but is not actually used
    num_rounds = 40

    # Rounds without continuation probability
    fixed_rounds = 2

    # Probability to continue the experiment for the next round
    cont_prob = 5/6


    maximum_price = 10
    monopoly_price = 10

    # Price that is recommended if there is a deviation from a player
    deviation_price = 1

    # Number of consumers
    m_consumer = 30

    # Treatment names
    treatments = ['baseline', 'recommendation']

    error_message_form_field = ('Ihre Antwort war leider nicht korrekt.' +
                                ' Bitte überlegen Sie noch einmal und lesen bei' +
                                ' Bedarf erneut in die Instruktionen.')

class Subsession(BaseSubsession):
    last_round =  models.IntegerField()
    def creating_session(self):
        if self.round_number == 1:
            # Initialize variable that shows if we still play
            self.session.vars['playing'] = True

            
            # We use itertools.cycle to have balanced treatments
            treatment_cycle = itertools.cycle(Constants.treatments)

            # Assign the treatment to each group
            # Note that we store it in the *treatment* field in the 
            # first round but also in the participant variables of
            # the first participant in the group to access it across rounds. 
            for g in self.get_groups():

                # If we have a fixed treatment for the session, use it for all groups
                # else assign the treatments in the iteration cycle.
                if 'group_treatment' in self.session.config:
                    treatment_draw = self.session.config['group_treatment']
                else:
                    treatment_draw = next(treatment_cycle)
                
                # Store it in the variable *group_treatment* for first round for the group
                g.group_treatment = treatment_draw

                # Furthermore, store it in the participant variables for the each player in each
                # group to access it accross rounds.
                for p in g.get_players():
                    p.participant.vars['group_treatment'] = treatment_draw

class Group(BaseGroup):
    winning_price = models.IntegerField()
    winner_profit = models.IntegerField()
    recommendation = models.IntegerField()
    n_winners = models.IntegerField()
    group_treatment  = models.StringField()

    def get_recommendation(self, round_number):
        """ Based on the past round create a new recommendation
        for the following period. 
        Currently, this recommendation is based on the following
        simple rule:
        - In the first round recommend the monopoly price
        - In all later round:
            - If all players followed the advise in the last round
            rounds, recommend the monopoly price
            - If player played different prices, recommend the deviation
            price
        
        """
        players = self.get_players()

        # If we are not in the first round, we recommend the monopoly price
        # if players had the same price in the last period
        # and else the deviation price
        if round_number > 1:
            past_prices = [p.in_previous_rounds()[-1].price for p in players]
            unique_prices = set(past_prices)
            if len(unique_prices) != 1:
                self.recommendation = Constants.deviation_price
            else:
                self.recommendation = Constants.monopoly_price
        else:
            # In the first round we always recommend the monopoly price
            self.recommendation = Constants.monopoly_price

    def set_profits_round(self):
        players = self.get_players()
        self.winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == self.winning_price]
        self.n_winners = len(winners)
        # Market is shared among all winners
        self.winner_profit = int(self.winning_price * Constants.m_consumer / self.n_winners)

        for p in players:
            if p in winners:
                p.is_winner = True
                p.profit = self.winner_profit
                p.accumulated_profit = sum([p_in_round.profit for p_in_round in p.in_all_rounds()])
            else:
                p.is_winner = False
                p.profit = 0
                p.accumulated_profit = sum([p_in_round.profit for p_in_round in p.in_all_rounds()])

    

class Player(BasePlayer):
    price = models.IntegerField(
        min=Constants.deviation_price, max=Constants.maximum_price,
        doc="""Price player offers to sell product for"""
    )

    # Define all as Integer as they are points/tokens
    # Round specific profit and accumulated profit as points
    profit = models.IntegerField()
    accumulated_profit = models.IntegerField()

    is_winner = models.BooleanField()


    # Final payoff is stored again
    final_payoff_euro = models.FloatField()


    # Quiz Questions
    q_how_many_customer = models.IntegerField(
        initial=None, 
        choices = [25, 35, 30, 40],
        label = 'Wie viele Kunden gibt es im Markt?'
    )

    q_after_fixed_round = models.StringField(
        initial=None, 
        choices = ['Das wird durch Würfeln entschieden.', 'Ja.', 'Nein.'],
        label='Endet das Experiment nach der 20. Runde?'
    )

    q_profit_1 = models.IntegerField(
        initial=None, 
        label='Sie sind Firma A und wählen einen Preis von 2, Firma B wählt einen Preis von 10,' +
              ' Firma C wählt einen Preis von 9. Was ist Ihr Gewinn in Talern?'
    )

    q_profit_2 = models.IntegerField(
        initial=None, 
        label='Sie sind Firma A und wählen einen Preis von 8, Firma B wählt einen Preis von 8, ' + 
               'Firma C wählt einen Preis von 8. Was ist Ihr Gewinn in Talern?'
    )

    q_profit_3 = models.FloatField(
        initial=None, 
        label='Sie haben einen Gewinn von 650 Talern, was ist Ihr Gewinn in €?'
    )

    q_goal_alg = models.StringField(
        initial=None, 
        choices = ['Gewinne für alle Firmen in einer einzelnen Runde zu maximieren.',
                   'Gesamtgewinne über alle Runden hinweg für alle Firmen zu maximieren.',
                   'Gesamtgewinne über alle Runden hinweg für einzelne Firmen zu maximieren.',
                   'Gewinne für einzelne Firmen in einer einzelnen Runde zu maximieren.'],
        label= 'Welches Ziel verfolgt der Algorithmus?'
    )

    # Counter variable how often the player has answered smth wrong
    counter_how_many_customer = models.IntegerField(initial = 0)
    counter_after_fixed_round = models.IntegerField(initial = 0)
    counter_q_profit_1 = models.IntegerField(initial = 0)
    counter_q_profit_2 = models.IntegerField(initial = 0)
    counter_q_profit_3 = models.IntegerField(initial = 0)
    counter_goal_alg = models.IntegerField(initial = 0, blank=True)


    # Error evaluation of form fields
    def q_how_many_customer_error_message(self, value):
        if value != 30:
            # Count +1 if the player answered the question wrong
            self.counter_how_many_customer += 1
            return Constants.error_message_form_field

    def q_after_fixed_round_error_message(self, value):
        if value != 'Das wird durch Würfeln entschieden.':
            # Count +1 if the player answered the question wrong
            self.counter_after_fixed_round += 1
            return Constants.error_message_form_field

    def q_profit_1_error_message(self, value):
        if value != 60:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_1 += 1
            return Constants.error_message_form_field

    def q_profit_2_error_message(self, value):
        if value != 80:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_2 += 1
            return Constants.error_message_form_field

    def q_profit_3_error_message(self, value):
        correct_answer = round(650 * self.session.config['real_world_currency_per_point'], 1)
        if value != correct_answer:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_3 += 1
            return Constants.error_message_form_field

    def q_goal_alg_error_message(self, value):
        if value != 'Gesamtgewinne über alle Runden hinweg für alle Firmen zu maximieren.':
            # Count +1 if the player answered the question wrong
            self.counter_goal_alg += 1
            return Constants.error_message_form_field

    def set_final_payoff(self):
        # We take the accumulated payoff from the last round we 
        # actually played
        last_played_round = self.session.vars['last_round']
        total_money = self.in_round(last_played_round).accumulated_profit 
        self.payoff = total_money
        # Final points as money
        self.final_payoff_euro = float(self.participant.payoff_plus_participation_fee())
