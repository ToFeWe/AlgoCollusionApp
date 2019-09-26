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
    def creating_session(self):
        if self.round_number == 1:
            if self.session.num_participants == 9:
                shuffle_structure = [[1,5,9], [4, 8, 3], [7, 2, 6]]
            elif self.session.num_participants == 18:
                shuffle_structure = [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                        [10, 14, 18], [13, 17, 12], [16, 11, 15]]
            elif self.session.num_participants == 27:
                shuffle_structure = [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                                    [10, 14, 18], [13, 17, 12], [16, 11, 15], 
                                    [19, 23, 27], [22, 26, 21], [25, 20, 24]]
            
            self.set_group_matrix(shuffle_structure)
        else:
            self.group_like_round(1)


class Group(SharedBaseGroup):
    pass


class Player(SharedBasePlayer):
    pass
