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
        return {#'round_number_draw': 17,
                'round_number_draw': 1, # for testing TODO: Remove
                'super_game_count': 2,
                'group_shuffle_by_size' : {
                    3: {'shuffle_structure_small': [[1,5,9], [4, 8, 3], [7, 2, 6]],
                        'shuffle_structure_medium': [[1, 5, 9], [4, 8, 3], [7, 2, 6],
                                                    [10, 14, 18], [13, 17, 12], [16, 11, 15]]
                        },
                    2: {'shuffle_structure_small': [[1,6], [3, 2], [5, 4]],
                        'shuffle_structure_medium': [[1,6], [3, 2], [5, 4],
                                                    [7,12], [9, 8], [11, 10]],
                        'shuffle_structure_big':  [[1,6], [3, 2], [5, 4],
                                                   [7,12], [9, 8], [11, 10],
                                                   [13,18], [15, 14], [17, 16]]
                    }
                } 
                }

class Group(SharedBaseGroup):
    pass


class Player(SharedBasePlayer):
    pass
