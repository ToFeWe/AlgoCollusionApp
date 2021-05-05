from bertrand.models import Constants as OriginalConstants, SharedBaseSubsession, SharedBaseGroup, SharedBasePlayer


class Constants(OriginalConstants):
    name_in_url = 'bertrand_SG_3'
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
        return {'round_number_draw': 11,
                #'round_number_draw': 2, # for testing TODO: Remove
                'super_game_count': 3,
                'group_shuffle_by_size' : {
                    3 : {'shuffle_structure_small': [[1, 6, 8], [4, 9, 2], [7, 3, 5]],
                         'shuffle_structure_medium': [[1, 6, 8], [4, 9, 2], [7, 3, 5],
                                                      [10, 15, 17], [13, 18, 11], [16, 12, 14]]
                        },
                    2: {'shuffle_structure_small': [[1,4], [3, 6], [5, 2]],
                        'shuffle_structure_medium': [[1,4], [3, 6], [5, 2],
                                                    [7,10], [9, 12], [11, 8]],
                        'shuffle_structure_big':  [[1,4], [3, 6], [5, 2],
                                                   [7,10], [9, 12], [11, 8],
                                                   [13,16], [15, 18], [17, 14]]
                    }
                } 
                } 
                
class Group(SharedBaseGroup):
    pass


class Player(SharedBasePlayer):
    pass
