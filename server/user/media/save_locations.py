from enum import Enum


class SDUserSaveLocations(Enum):
    """Enum for valid save locations"""
    picture = 'User Picture'

    @classmethod
    def choices(cls):
        """
        Gets the choices in tuple form
        :return: App name and value in tuple for
        """
        return tuple((location.name, location.value) for location in cls)