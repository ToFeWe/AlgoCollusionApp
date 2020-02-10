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
    def this_app_constants(self):
        """ App specific constants
        
        """
        # The number of rounds we have drawn ex ante according to some cont prob
        return {'round_number_draw': 8,
                'super_game_count': 2,
                'shuffle_structure_small': [[1,5,9], [4, 8, 3], [7, 2, 6]],
                'shuffle_structure_medium': [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                                            [10, 14, 18], [13, 17, 12], [16, 11, 15]],
                'shuffle_structure_big': [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                                    [10, 14, 18], [13, 17, 12], [16, 11, 15], 
                                    [19, 23, 27], [22, 26, 21], [25, 20, 24]],
                'shuffle_structure_full': [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                                    [10, 14, 18], [13, 17, 12], [16, 11, 15], 
                                    [19, 23, 27], [22, 26, 21], [25, 20, 24],
                                    [28, 32, 36], [31, 35, 30], [34, 29, 33]]

                } 

class Group(SharedBaseGroup):
    pass


class Player(SharedBasePlayer):
    pass
