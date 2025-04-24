from enum import Enum

class CardTypes(Enum):
    ARTIFACT = 'artifact'
    BATTLE = 'battle'
    CARD = 'card'
    CREATURE = 'creature'
    ENCHANTMENT = 'enchantment'
    INSTANT = 'instant'
    LAND = 'land'
    PLANESWALKER = 'planeswalker'
    SORCERY = 'sorcery'
    OTHER = 'other'

class SuperTypes(Enum):
    BASIC = 'basic'
    LEGENDARY = 'legendary'
    ONGOING = 'ongoing'
    SNOW = 'snow'
    WORLD = 'world'

class TypeLineDelimiters(Enum):
    MULTI_FACE = '//'
    SUBTYPE = '—'


