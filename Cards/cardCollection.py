class CardCollection:
    def __init__(self, image_size):
        self._cards = {}
        self._image_size = image_size

    @property
    def cards(self):
        return self._cards