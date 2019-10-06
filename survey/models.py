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
    def creating_session(self):
        # For testing purposes only # TODO: Delete later again
        for p in self.get_players():
            if 'group_treatment' not in p.participant.vars.keys():
                p.participant.vars['group_treatment'] = self.session.config['group_treatment']

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
        label='Nehmen Sie an, dass Sie keine Empfehlung bekommen hätten. Denken Sie, dass Ihr Gesamtgewinn höher oder niedriger gewesen wäre?',
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


    q_alg_improve = models.StringField(
        initial=None,
        label='Könnte man Ihrer Meinung nach den Algorithmus optimieren? Wenn ja wie?'
    )
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

    # Socially appropriate
    q_socially_appropriate_10 =  models.StringField(
        initial=None,
        choices=['sehr sozial unangemessen', 'etwas sozial unangemessen',
                 'etwas sozial angemessen', 'sehr sozial angemessen'],
        label='... 10 Talern zu wählen?',
        widget=widgets.RadioSelectHorizontal())

    q_socially_appropriate_9 =  models.StringField(
        initial=None,
        choices=['sehr sozial unangemessen', 'etwas sozial unangemessen',
                 'etwas sozial angemessen', 'sehr sozial angemessen'],
        label='... 9 Talern zu wählen?',
        widget=widgets.RadioSelectHorizontal())

    q_socially_appropriate_1 =  models.StringField(
        initial=None,
        choices=['sehr sozial unangemessen', 'etwas sozial unangemessen',
                 'etwas sozial angemessen', 'sehr sozial angemessen'],
        label='... 1 Taler zu wählen?',
        widget=widgets.RadioSelectHorizontal())

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
    q_other_notes = models.StringField(blank=True, label="Haben Sie weitere abschließende Anmerkungen zu diesem Experiment?")
    
    # Falk Questions

    # Risk
    q_falk1 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht risikobereit'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr risikobereit')],
        verbose_name='Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        doc="""Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?""",
        widget=widgets.RadioSelectHorizontal())

    # Time
    q_falk2 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht bereit zu verzichten'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr bereit zu verzichten')],
        verbose_name='Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?',
        doc="""Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?""",
        widget=widgets.RadioSelectHorizontal())

    # Trust
    q_falk3 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'trifft voll zu')],
        verbose_name='Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.',
        doc="""Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.""",
        widget=widgets.RadioSelectHorizontal())

    # Neg. Rec.
    q_falk4 = models.CharField(
        initial=None,
        choices=[('0', 'gar nicht bereit zu bestrafen'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'sehr bereit zu bestrafen')],
        verbose_name='Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?',
        doc="""Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?""",
        widget=widgets.RadioSelectHorizontal())

    # Pos. Rec.
    q_falk5 = models.CharField(
        initial=None,
        choices=[('0', 'trifft gar nicht zu'),
                 ('1', ''),
                 ('2', ''),
                 ('3', ''),
                 ('4', ''),
                 ('5', ''),
                 ('6', ''),
                 ('7', ''),
                 ('8', ''),
                 ('9', ''),
                 ('10', 'trifft voll zu')],
        verbose_name='Wenn mir jemand einen Gefallen tut, bin ich bereit, diesen zu erwidern.',
        doc="""Wenn mir jemand einen Gefallen tut, bin ich bereit, diesen zu erwidern.""",
        widget=widgets.RadioSelectHorizontal())
