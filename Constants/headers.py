from enum import Enum

class CSVHeaders(Enum):
    SCRYFALL_ID = 'scryfall id'
    QUANTITY = 'quantity'
    NAME = 'name'
    SET_NAME = 'set name'

class APIResponseHeaders(Enum):
    COLOR_IDENTITY = 'color_identity'
    CARD_FACES = 'card_faces'
    IMAGE_URIS = 'image_uris'
    FACE_NAME = 'name'
    SET_NAME = 'set_name'
    LAYOUT = 'layout'
    TYPE_LINE = 'type_line'

    @staticmethod
    def get_double_sided_layouts():
        return ['transform', 'modal_dfc', 'double_faced_token']