from enum import Enum

class ColorIdentity(Enum):
    W = 'White'
    U = 'Blue'
    B = 'Black'
    R = 'Red'
    G = 'Green'
    C = 'Colorless'


    @staticmethod
    def to_sorted_list(colors):
        if len(colors) == 0:
            return [ColorIdentity.C.value]

        lst = []
        for color_identity in ColorIdentity:
            if color_identity.name in colors:
                lst.append(color_identity.value)

        lst.sort()
        return lst

    @staticmethod
    def construct_named_identity(colors):
        return '-'.join(colors)