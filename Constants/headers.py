from enum import StrEnum, auto

class CSVHeaders(StrEnum):
    SCRYFALL_ID = 'scryfall id'
    QUANTITY = auto()
    NAME = auto()
    SET_NAME = 'set name'
    RARITY = auto()

class APIResponseHeaders(StrEnum):
    COLOR_IDENTITY = auto()
    CARD_FACES = auto()
    IMAGE_URIS = auto()
    FACE_NAME = auto()
    SET_NAME = auto()
    LAYOUT = auto()
    TYPE_LINE = auto()
    RARITY = auto()

    @staticmethod
    def get_double_sided_layouts():
        return ['transform', 'modal_dfc', 'double_faced_token']
