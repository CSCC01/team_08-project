from enum import Enum


#  The Roles a user can have
class Roles(Enum):
    RO = "Restaurant Owner"
    BU = "Basic User"

    @classmethod
    def choices(cls):
        return tuple((role.name, role.value) for role in cls)
