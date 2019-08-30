from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Question for the treatment
    q_alg_helpful = models.StringField(
        initial=None,
        choices=[('0', 'gar nicht hilfreich'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr hilfreich')],
        label='Wie hilfreich fanden Sie die Empfehlungen des Algorithmus?',
        widget=widgets.RadioSelectHorizontal())

    q_alg_how_sure = models.StringField(
        initial=None,
        choices=[('0', 'gar nicht sicher'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr sicher')],
        label='Wie sicher waren Sie sich, dass Ihre Mitspieler der Empfehlung des Algorithmus folge leisten würden?',
        widget=widgets.RadioSelectHorizontal())

    q_alg_no_recommendation = models.StringField(
        initial=None,
        choices=[('0', 'deutlich niedriger'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'deutlich höher')],
        label='Nehmen Sie an, dass Sie keine Empfehlung bekommen hätten. Denken Sie, dass Ihr Gesamtgewinn höher oder niedriger gewesen wäre? ',
        widget=widgets.RadioSelectHorizontal())

    q_alg_relevant_other_player = models.StringField(
        initial=None,
        choices=[('0', 'gar nicht hilfreich'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr hilfreich')],
        label='Was denken Sie, wie relevant war die Empfehlung des Algorithmus für Ihre Mitspieler?',
        widget=widgets.RadioSelectHorizontal())

    # Questions for all    
    q_all_other_players = models.StringField(
        initial=None,
        choices=[('0', 'gar nicht abhängig'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr stark abhängig')],
        label='Wie sehr war Ihre Preisentscheidung von den Preisentscheidungen Ihrer Mitspieler in der letzten Runde abhängig?',
        widget=widgets.RadioSelectHorizontal())

    q_all_communication = models.StringField(
        initial=None,
        choices=['Ja.', 'Nein.', 'Ich weiß es nicht.'],
        label='Hätten Sie sich gewünscht Sie könnten mit Ihren Mitspielern kommunizieren?')

    # General Questions
    q_age = models.IntegerField(label='Wie alt sind Sie?', min=12, max=99)
    q_gender = models.StringField(
        label = 'Was ist Ihr Geschlecht?',
        choices = ['Männlich', 'Weiblich', 'Divers', 'keine Angabe']
    )
    q_study_field = models.StringField(label='Was studieren Sie?')
    q_semester = models.IntegerField(label='Im wievielten Semester studieren Sie?', min=1, max=45)
    q_n_experiment = models.IntegerField(label='An wie vielen Experimenten haben Sie bereits teilgenommen?')
    q_similar_experiment = models.StringField(label='Haben Sie schon einmal an einem ähnlichen Experiment teilgenommen?',
                                         choices=['Ja.', 'Nein.', 'Ich weiß es nicht.'])
