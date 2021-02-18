from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Tobias Werner'

doc = """ An App for a price recommendation system in a market experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'introduction'
    # Group only needed later in the market game
    players_per_group = None
    num_rounds = 1


    maximum_price = 5
    reservation_price = 4
    stage_game_NE = 1
    lowest_price = 0 

    
    # Number of consumers
    m_consumer = 60

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
                p.treatment = self.session.config['group_treatment']

                # We have a participant variable to record if the participant dropped out of 
                # the experiment, to be able to replace him/her with a bot
                p.participant.vars['is_dropout'] = False

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.StringField()

    # TODO: add it to this app
    is_dropout = models.BooleanField()
    
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

    q_profit_3 = models.FloatField(
        initial=None, 
        label='Sie haben einen Gewinn von 650 Talern, was ist Ihr Gewinn in Euro?'
    )

    # Counter variable how often the player has answered smth wrong
    counter_how_many_customer = models.IntegerField(initial = 0)
    counter_after_fixed_round = models.IntegerField(initial = 0)
    counter_consumer_wtp = models.IntegerField(initial = 0)
    counter_q_profit_1 = models.IntegerField(initial = 0)
    counter_q_profit_2 = models.IntegerField(initial = 0)
    counter_q_profit_3 = models.IntegerField(initial = 0)
    

    # Error evaluation of form fields
    def q_how_many_customer_error_message(self, value):
        if value != Constants.m_consumer:
            # Count +1 if the player answered the question wrong
            self.counter_how_many_customer += 1
            self.q_after_fixed_round
            return Constants.error_message_form_field

    def q_after_fixed_round_error_message(self, value):
        if value != '95%':
            # Count +1 if the player answered the question wrong
            self.counter_after_fixed_round += 1
            return Constants.error_message_form_field

    def q_consumer_wtp_error_message(self, value):
        if value != Constants.reservation_price:
            self.counter_consumer_wtp += 1
            return Constants.error_message_form_field


    def q_profit_1_error_message(self, value):
        if value != 60:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_1 += 1
            return Constants.error_message_form_field

    def q_profit_2_error_message(self, value):
        # The correct answer here depends on the number of firms in the market
        # which is different for different treatments.
        if self.session.config['group_treatment'] in ['1H1A', '2H0A']:
            # 60 * 3 / 2 = 90
            correct_answer = 90
        else:
            # 60 * 3 / 3 = 60
            correct_answer = 60
        if value != correct_answer:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_2 += 1
            return Constants.error_message_form_field

    def q_profit_3_error_message(self, value):
        correct_answer = round(650 * self.session.config['real_world_currency_per_point'], 1)
        if value != correct_answer:
            # Count +1 if the player answered the question wrong
            self.counter_q_profit_3 += 1
            return Constants.error_message_form_field
