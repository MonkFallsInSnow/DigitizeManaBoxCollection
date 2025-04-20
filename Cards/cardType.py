from Constants.type_data import CardTypes
from Constants.type_data import TypeLineDelimiters
class CardType:
    def __init__(self, type_line):
        self._type_line = type_line.lower()
        self._type_data = self._parse_type_line()

    # TODO: deal with subtypes, if you feel like it...
    def _parse_type_line(self):
        type_data = {'front': [], 'back': [], 'legendary': False}
        type_line  = self._type_line

        if CardTypes.LEGENDARY.value in self._type_line:
            type_data[CardTypes.LEGENDARY.value] = True
            type_line = type_line.replace(CardTypes.LEGENDARY.value, '')

        if TypeLineDelimiters.MULTI_FACE.value in type_line:
            front_types, back_types = type_line.split(TypeLineDelimiters.MULTI_FACE.value)
            front_types, _ = front_types.split(TypeLineDelimiters.SUBTYPE.value)
            back_types, _ = back_types.split(TypeLineDelimiters.SUBTYPE.value)

            front_types = front_types.split()
            back_types = back_types.split()
            #type_data['subtypes'] = ''.join([front_subtype, back_subtype]).split()

            #back_types, subtype = back_types.split(TypeLineDelimiters.SUBTYPE.value)
            #type_data['subtypes'].append(subtype)

            type_data['front'] = CardTypes.validate_types(front_types)
            type_data['back'] = CardTypes.validate_types(back_types)
        elif TypeLineDelimiters.SUBTYPE.value in type_line:
            front_types, _ = type_line.split(TypeLineDelimiters.SUBTYPE.value)
            front_types = front_types.split()
            type_data['front'] = CardTypes.validate_types(front_types)
        else:
            type_data['front'].append(type_line)


        return type_data

    def __str__(self):
        return str(self._type_data)
