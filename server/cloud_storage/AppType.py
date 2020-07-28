from enum import Enum


class AppCollection(Enum):
    """ Different possible application """
    RE_F = "restaurant/FoodMedia"
    # RE_RE = 'restaurant/restaurant'
    # U = 'user'

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: App name and value in tuple for
        """
        return tuple((role.value, role.name) for role in cls)