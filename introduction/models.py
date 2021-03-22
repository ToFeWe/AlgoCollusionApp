from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from bertrand.models import Constants as ConstantsBertrand


author = 'Tobias Werner'

doc = """ An App for a price recommendation system in a market experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'introduction'
    # Group only needed later in the market game
    players_per_group = None
    num_rounds = 1

    # Load constants from main app
    maximum_price = ConstantsBertrand.maximum_price
    reservation_price = ConstantsBertrand.reservation_price
    stage_game_NE = ConstantsBertrand.stage_game_NE
    lowest_price = ConstantsBertrand.lowest_price
    m_consumer = ConstantsBertrand.m_consumer

    # Timeout info
    # Timeouts in seconds
    # The timeouts are longer here as participants have to read instructions etc
    # which might take longer.
    #timeout_soft = 6 * 60 # After 6 minutes the timeout is shown and participants get a notification
    #timeout_hard = 7 * 60 # After 7 minutes auto-submitted
    timeout_soft = 20
    timeout_hard = 40

    timeout_text = ("Bitte klicken Sie auf Weiter, sobald Sie die Insturktionen gelesen haben. Sollten Sie das Zeitlimit "
                   "überschreiten, werden Sie aus dem Experiment ausgeschlossen. Verbleibende Zeit:")


    error_message_form_field = ('Ihre Antwort war leider nicht korrekt.' +
                                ' Bitte überlegen Sie noch einmal und lesen bei' +
                                ' Bedarf erneut in die Instruktionen.')


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            # Every player is in the same treatment for now.
            # Thus, we cannot/shouldnot run baseline and treatment in the same session.
            for p in self.get_players():
                # Save treatment in participant vars for future apps and also in formfield for
                # analysis.
                p.participant.vars['group_treatment'] = self.session.config['group_treatment']
                p.group.group_treatment = self.session.config['group_treatment']
                
                # We have a participant variable to record if the participant dropped out of 
                # the experiment, to be able to replace him/her with a bot
                p.participant.vars['is_dropout'] = False

class Group(BaseGroup):
    group_treatment = models.StringField()

    def get_additional_template_variables(self):
        """
        Simple helper method that returns information for the template, which are mainly
        used in the instructions.

        """
        n_players = 2 if self.group_treatment in ['2H0A', '1H1A'] else 3
        group_treatment = self.group_treatment
        algo_treatment = True if group_treatment not in ['2H0A', '3H0A'] else False
        return {
            'algo_treatment': algo_treatment,
            'group_treatment': group_treatment,
            'n_players': n_players,
            'exchange_rate': 1 / self.session.config['real_world_currency_per_point'],
            'show_up': self.session.config['participation_fee']
        }

class Player(BasePlayer):

    treatment = models.StringField()

    is_dropout = models.BooleanField()

    def record_dropout(self):
        """ Small helper function to record that a player dropout. """
        self.participant.vars['is_dropout'] = True
        self.is_dropout = True

    # Quiz Questions
    q_how_many_customer = models.IntegerField(
        initial=None, 
        choices = [35, 30, 40, 60],
        label = 'Wie viele Kunden gibt es im Markt, die das Produkt kaufen wollen?'
    )

    q_after_fixed_round = models.StringField(
        initial=None, 
        choices = ['95%', '5%', '50%'],
        label='Was ist die Wahrscheinlichkeit, dass nach Abschluss einer Periode eine weitere gespielt wird?'
    )

    q_consumer_wtp = models.IntegerField(initial=None,
        label="Was ist der maximale Preis, den die Kunden bereit sind für das Produkt zu zahlen?")
    
    q_profit_1 = models.IntegerField(
        initial=None
        # Note: Made treatment specific directly in the template
        # label='Sie sind Firma A und wählen einen Preis von 2, Firma B wählt einen Preis von 3,' +
        #       ' Firma C wählt einen Preis von 5. Was ist Ihr Gewinn in Talern in dieser Runde?'
    )

    q_profit_2 = models.IntegerField(
        initial=None
        # Note: Made treatment specific directly in the template
        # label='Sie sind Firma A und wählen einen Preis von 3, Firma B wählt einen Preis von 3, ' + 
        #        'Firma C wählt einen Preis von 3. Was ist Ihr Gewinn in Talern in dieser Runde?'
    )

    # Counter variable how often the player has answered smth wrong
    counter_how_many_customer = models.IntegerField(initial = 0)
    counter_after_fixed_round = models.IntegerField(initial = 0)
    counter_consumer_wtp = models.IntegerField(initial = 0)
    counter_q_profit_1 = models.IntegerField(initial = 0)
    counter_q_profit_2 = models.IntegerField(initial = 0)
    
    # Evaluation if some questions have been answered incorrect three times
    # In this case I will show the correct answers to the participants.
    three_times_wrong = models.BooleanField(initial=False)

    def check_three_times_wrong(self):
        all_values = [self.counter_how_many_customer,
                      self.counter_after_fixed_round,
                      self.counter_consumer_wtp,
                      self.counter_q_profit_1,
                      self.counter_q_profit_2
                      ]

        self.three_times_wrong = any(v >= 3 for v in all_values)

    # Error evaluation of form fields
    def q_how_many_customer_error_message(self, value):
        if value != Constants.m_consumer:
            # Count +1 if the player answered the question wrong
            self.counter_how_many_customer += 1
            self.q_after_fixed_round

            # If less than three times wrong, show error message
            # Else we skip the page.
            self.check_three_times_wrong()
            if not self.three_times_wrong:
                return Constants.error_message_form_field

    def q_after_fixed_round_error_message(self, value):
        if value != '95%':
            # Count +1 if the player answered the question wrong
            self.counter_after_fixed_round += 1

            # If less than three times wrong, show error message
            # Else we skip the page.
            self.check_three_times_wrong()
            if not self.three_times_wrong:
                return Constants.error_message_form_field

    def q_consumer_wtp_error_message(self, value):
        if value != Constants.reservation_price:
            self.counter_consumer_wtp += 1

            # If less than three times wrong, show error message
            # Else we skip the page.
            self.check_three_times_wrong()
            if not self.three_times_wrong:
                return Constants.error_message_form_field


    def q_profit_1_error_message(self, value):
        if value != 60:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_1 += 1

            # If less than three times wrong, show error message
            # Else we skip the page.
            self.check_three_times_wrong()
            if not self.three_times_wrong:
                return Constants.error_message_form_field

    def q_profit_2_error_message(self, value):
        # The correct answer here depends on the number of firms in the market
        # which is different for different treatments.
        if self.group.group_treatment in ['1H1A', '2H0A']:
            # 60 * 3 / 2 = 90
            correct_answer = 90
        else:
            # 60 * 3 / 3 = 60
            correct_answer = 60
        if value != correct_answer:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_2 += 1

            # If less than three times wrong, show error message
            # Else we skip the page.
            self.check_three_times_wrong()
            if not self.three_times_wrong:
                return Constants.error_message_form_field