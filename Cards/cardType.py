from Constants.cardTypes import CardTypes, SuperTypes, TypeLineDelimiters
from Cards.cardTypeData import CardTypeData

class CardType:
    def __init__(self, type_line):
        self._type_line = type_line.lower()
        self._type_data = self._parse_type_line()

    @property
    def type_data(self):
        return self._type_data

    def _parse_type_line(self):
        if TypeLineDelimiters.MULTI_FACE not in self._type_line:
            type_data = self._get_single_face_types()
        else:
            type_data = self._get_multi_face_types()

        return type_data

    def _get_single_face_types(self):
        if TypeLineDelimiters.SUBTYPE not in self._type_line:
            front_face_type_line = self._type_line
            front_face_subtype_line = ''
        else:
            front_face_type_line, front_face_subtype_line = self._type_line.split(TypeLineDelimiters.SUBTYPE)

        front_face_supertypes = CardType._extract_supertypes(front_face_type_line)
        front_face_types = CardType._extract_types(front_face_type_line)
        front_face_subtypes = front_face_subtype_line.split()

        return CardTypeData(
            front_face_supertypes=front_face_supertypes,
            front_face_types=front_face_types,
            front_face_subtypes=front_face_subtypes
        )

    def _get_multi_face_types(self):
        front_face_type_line, back_face_type_line = self._type_line.split(TypeLineDelimiters.MULTI_FACE)
        front_face_supertypes = CardType._extract_supertypes(front_face_type_line)
        back_face_supertypes = CardType._extract_supertypes(back_face_type_line)

        if TypeLineDelimiters.SUBTYPE not in front_face_type_line:
            front_face_types = front_face_type_line
            front_face_subtypes = ''
        else:
            front_face_types, front_face_subtypes = front_face_type_line.split(TypeLineDelimiters.SUBTYPE)

        if TypeLineDelimiters.SUBTYPE not in back_face_type_line:
            back_face_types = back_face_type_line
            back_face_subtypes = ''
        else:
            back_face_types, back_face_subtypes = back_face_type_line.split(TypeLineDelimiters.SUBTYPE)

        front_face_types = CardType._extract_types(front_face_types)
        front_face_subtypes = front_face_subtypes.split()
        back_face_types = CardType._extract_types(back_face_types)
        back_face_subtypes = back_face_subtypes.split()

        return CardTypeData(
            front_face_supertypes=front_face_supertypes,
            front_face_types=front_face_types,
            front_face_subtypes=front_face_subtypes,
            back_face_supertypes=back_face_supertypes,
            back_face_types=back_face_types,
            back_face_subtypes=back_face_subtypes
        )

    @staticmethod
    def _extract_supertypes(type_line_component):
        return CardType._get_type(type_line_component, SuperTypes, SuperTypes.BASIC.value)

    @staticmethod
    def _extract_types(type_line_component):
        return CardType._get_type(type_line_component, CardTypes, CardTypes.OTHER.value)

    @staticmethod
    def _get_type(type_line_component, type_kind, default):
        types = []
        type_line_component = type_line_component.split()

        for component in type_line_component:
            for kind in type_kind:
                if component == kind.value and component not in TypeLineDelimiters:
                    types.append(kind.value)

        if len(types) == 0:
            types.append(default)

        return types

    def __str__(self):
        return str(self._type_data)
