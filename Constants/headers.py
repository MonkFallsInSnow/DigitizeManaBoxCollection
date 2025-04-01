from enum import Enum

class CSVHeaders(Enum):
    SCRYFALL_ID = 'scryfall id'
    QUANTITY = 'quantity'
    NAME = 'name'
    SET_NAME = 'set name'

class ResponseHeaders(Enum):
    COLOR_IDENTITY = 'color_identity'
    CARD_FACES = 'card_faces'
    IMAGE_URIS = 'image_uris'
    FACE_NAME = 'name'