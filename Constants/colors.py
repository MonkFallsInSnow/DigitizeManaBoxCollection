from enum import StrEnum

class ColorIdentity(StrEnum):
    W = 'White'
    U = 'Blue'
    B = 'Black'
    R = 'Red'
    G = 'Green'
    C = 'Colorless'


    @staticmethod
    def to_value_list(colors):
        if len(colors) == 0:
            return [ColorIdentity.C]

        lst = []
        for color_identity in ColorIdentity:
            if color_identity.name in colors:
                lst.append(color_identity.value)

        return lst

    @staticmethod
    def to_verbose_color_identity(colors):
        sorted_list = sorted(ColorIdentity.to_value_list(colors))
        return '-'.join(sorted_list)
