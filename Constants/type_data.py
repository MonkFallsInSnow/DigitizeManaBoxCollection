from enum import Enum

class CardTypes(Enum):
    ARTIFACT = 'artifact'
    BATTLE = 'battle'
    CARD = 'card'
    CREATURE = 'creature'
    ENCHANTMENT = 'enchantment'
    INSTANT = 'instant'
    LAND = 'land'
    LEGENDARY = 'legendary'
    PLANESWALKER = 'planeswalker'
    SORCERY = 'sorcery'

    @staticmethod
    def clean_data(data):
        return data.strip()

    @staticmethod
    def validate_types(data, default='other'):
        for i in range(len(data)):
            if data[i] not in CardTypes:
                data[i] = default

        return data


class TypeLineDelimiters(Enum):
    MULTI_FACE = '//'
    SUBTYPE = '—'


