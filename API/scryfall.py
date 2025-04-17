import functools
import random
import asyncio
import aiohttp
import logging
import json
from tqdm.asyncio import tqdm as async_tqdm
from Cards.card import Card
from Constants.headers import CSVHeaders, APIResponseHeaders

class ScryfallAPI:
    BASE_URL = 'https://api.scryfall.com/cards'

    @staticmethod
    def rate_limiter(func):
        """
        A decorator that adds a small random delay before executing
        an asynchronous function to implement simple rate limiting.
        """

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(random.uniform(0.02, 0.05))
            return await func(*args, **kwargs)

        return wrapper

    #TODO: implement the ability to fetch a single card later, if you feel like it...
    # @staticmethod
    # def fetch_card(scryfall_id, csv_data, image_size):
    #     pass

    @staticmethod
    async def fetch_all_cards(csv_data, image_size='normal', concurrency_limit=25):
        """
        Fetch all cards from Scryfall API and return as Card objects

        Args:
            csv_data: Dictionary of card data from CSV
            image_size: Size of images to fetch ('small', 'normal', 'large', etc.)
            concurrency_limit: Maximum number of concurrent requests

        Returns:
            List of Card objects
        """
        async with aiohttp.ClientSession() as session:
            # Create a semaphore for concurrency control
            semaphore = asyncio.Semaphore(concurrency_limit)

            # Create tasks for all cards
            tasks = []
            for scryfall_id, card_data in csv_data.items():
                # Create bounded fetch task
                async def bounded_fetch(sid, data):
                    async with semaphore:
                        # Construct URLs
                        url = f'{ScryfallAPI.BASE_URL}/{sid}'
                        image_front_url = f'{url}?format=image&version={image_size}'
                        image_back_url = f'{image_front_url}&face=back'

                        # Fetch card data and create Card object
                        return await ScryfallAPI._fetch_card_async(
                            session=session,
                            url=url,
                            image_front_url=image_front_url,
                            image_back_url=image_back_url,
                            scryfall_id=sid,
                            csv_data=data,
                            image_size=image_size
                        )

                tasks.append(bounded_fetch(scryfall_id, card_data))

            # Process tasks with progress bar
            results = []
            for task in async_tqdm.as_completed(tasks, total=len(tasks), desc="Fetching cards"):
                card = await task
                if card:
                    results.append(card)

            return results

    @staticmethod
    @rate_limiter
    async def _fetch_card_async(session, url, image_front_url, image_back_url, scryfall_id, csv_data, image_size):
        try:
            # Get card data from Scryfall API
            async with session.get(url) as response:
                if response.status != 200:
                    logging.error(f"Failed to fetch card data for {scryfall_id}: HTTP {response.status}")
                    return None

                card_data = await response.json()

                # Extract relevant fields
                name = card_data.get(APIResponseHeaders.FACE_NAME.value, csv_data.get(CSVHeaders.NAME.value, 'Unknown'))
                set_name = card_data.get(APIResponseHeaders.SET_NAME.value, csv_data.get(CSVHeaders.SET_NAME.value, 'Unknown Set'))
                color_identity = card_data.get(APIResponseHeaders.COLOR_IDENTITY.value, [])

                # Get quantity from CSV data
                quantity = csv_data.get(CSVHeaders.QUANTITY.value, 1)

                # Get front image
                front_image = await ScryfallAPI._fetch_card_image_async(session, image_front_url)

                # Check if card has back face
                has_back_face = card_data.get(APIResponseHeaders.LAYOUT.value) in APIResponseHeaders.get_double_sided_layouts()
                # has_back_face = (
                #         card_data.get(APIResponseHeaders.CARD_FACES.value) is not None and
                #         len(card_data.get(APIResponseHeaders.CARD_FACES.value, [])) > 1 and
                #         APIResponseHeaders.IMAGE_URIS.value in card_data.get(APIResponseHeaders.CARD_FACES.value, [{}])[1]
                # ) or card_data.get(APIResponseHeaders.LAYOUT.value) in APIResponseHeaders.get_double_sided_layouts()

                # Get back image if exists
                back_image = None
                if has_back_face:
                    back_image = await ScryfallAPI._fetch_card_image_async(session, image_back_url)

                # Create and return card object
                return Card(
                    scryfall_id=scryfall_id,
                    quantity=quantity,
                    name=name,
                    set_name=set_name,
                    color_identity=color_identity,
                    front_image=front_image,
                    back_image=back_image
                )

        except aiohttp.ClientError as e:
            logging.error(f"Network error while fetching card {scryfall_id}: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON response for card {scryfall_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error processing card {scryfall_id}: {e}")
            return None

    @staticmethod
    @rate_limiter
    async def _fetch_card_image_async(session, url):
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    logging.warning(f"Failed to fetch card image from {url}: HTTP {response.status}")
                    return None

                return await response.read()

        except aiohttp.ClientError as e:
            logging.error(f"Network error while fetching image from {url}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error fetching image from {url}: {e}")
            return None
