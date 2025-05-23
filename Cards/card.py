from .cardType import CardType

class Card:
    def __init__(self, scryfall_id, quantity=1, name=None, set_name=None, rarity='', color_identity=None,
                 type_line='', front_image=None, back_image=None):
        self._scryfall_id = scryfall_id
        self._quantity = quantity
        self._name = name
        self._set_name = set_name
        self._rarity = rarity
        self._color_identity = color_identity
        self._card_types = CardType(type_line)
        self._front_image = front_image
        self._back_image = back_image

    # Property getters and setters
    @property
    def scryfall_id(self):
        return self._scryfall_id

    @property
    def quantity(self):
        return self._quantity

    @property
    def name(self):
        return self._name

    @property
    def set_name(self):
        return self._set_name

    @property
    def rarity(self):
        return self._rarity

    @property
    def color_identity(self):
        return self._color_identity

    @property
    def card_types(self):
        return self._card_types
    
    @property
    def front_image(self):
        return self._front_image

    @property
    def back_image(self):
        return self._back_image

    @property
    def has_multiple_faces(self):
        return False if self._back_image is None else True

    def __str__(self):
        return f'Name: {self._name}\nQuantity: {self._quantity}\nSet: {self.set_name}\n'\
               f'Rarity: {self._rarity}\nColor Identity: {self._color_identity}\n'\
               f'Card Type(s): {self._card_types}'