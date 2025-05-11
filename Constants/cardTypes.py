from enum import StrEnum, auto

class SuperTypes(StrEnum):
    BASIC = auto()
    LEGENDARY = auto()
    ONGOING = auto()
    SNOW = auto()
    WORLD = auto()

class CardTypes(StrEnum):
    ARTIFACT = auto()
    BATTLE = auto()
    CARD = auto()
    CREATURE = auto()
    ENCHANTMENT = auto()
    INSTANT = auto()
    LAND = auto()
    PLANESWALKER = auto()
    SORCERY = auto()
    OTHER = auto()

class TypeLineDelimiters(StrEnum):
    MULTI_FACE = '//'
    SUBTYPE = '—'
