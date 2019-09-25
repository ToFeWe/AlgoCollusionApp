from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1

    # TODO: Chekc that its always the same in the next app
    fixed_rounds = 1

    # TODO: Must check that those are the same as in the other app
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
    def creating_session(self):
        if self.round_number == 1:
            # Every player is in the same treatment for now.
            # Thus, we cannot run baseline and treatment in the same session.
            # Should be fine though.
            for p in self.get_players():
                # Save treatment in participant vars for future apps and also in formfield for
                # analysis.
                p.participant.vars['group_treatment'] = self.session.config['group_treatment']
                p.treatment = self.session.config['group_treatment']

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.StringField()

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