import asyncio
import logging
from API.scryfall import ScryfallAPI

class CardCollection:
    def __init__(self, image_size):
        self._cards = {}
        self._image_size = image_size

    @property
    def cards(self):
        return self._cards

    @property
    def image_size(self):
        return self._image_size

    def build_collection(self, csv_data):
        try:
            cards = asyncio.run(ScryfallAPI.fetch_all_cards(csv_data, self._image_size))

            for card in cards:
                self._cards[card.scryfall_id] = card

            logging.info(f"Collection built with {len(self._cards)} cards")
        except Exception as e:
            logging.error(f"Error building collection: {e}")

    def __str__(self):
        result = ''

        for data in self._cards.values():
            result += f'{data}\n\n'

        return f'Collection:\n{result}'