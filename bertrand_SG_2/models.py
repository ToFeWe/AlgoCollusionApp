from bertrand.models import Constants as OriginalConstants, SharedBaseSubsession, SharedBaseGroup, SharedBasePlayer


class Constants(OriginalConstants):
    name_in_url = 'bertrand_SG_2'
    # you can define new constants, but
    # don't override constants from the original app here.
    # if the 2 apps need to have different values for same-named constants,
    # you should make a "fake constants" method on the subsession of both apps, e.g.
    # def this_app_constants(self):
    #     return {'abc': 1, 'def': 2}
    # then instead of Constants.abc, do self.subsession.this_app_constants().abc
    # even better, return a NamedTuple instead of a dict.


class Subsession(SharedBaseSubsession):
    pass


class Group(SharedBaseGroup):
    pass


class Player(SharedBasePlayer):
    pass
