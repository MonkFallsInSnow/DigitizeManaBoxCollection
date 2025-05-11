import logging
from Arguments.arguments import parse_arguments
from DataManagers.dataHandler import DataHandler
from Cards.cardCollection import CardCollection

def setup_logging():
    '''Set up logging configuration'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('Logs/card_digitizer.log'),
            logging.StreamHandler()
        ]
    )

def main():
    try:
        setup_logging()
        logging.info('Starting MTG Card Digitizer')

        # Parse command line arguments
        args = parse_arguments()
        logging.info(f'Supplied arguments: {args}')

        # Read and clean CSV data
        logging.info(f'Reading card data from {args.input_csv}...')
        try:
            data_handler = DataHandler(args.input_csv)
            csv_data = data_handler.get_data()
            logging.info(f'Found {len(csv_data)} unique scryfall ids in {args.input_csv}')

            # Build collection
            logging.info(f"Building card collection...")
            collection = CardCollection(args.image_size)
            collection.build_collection(csv_data)
            logging.info(f"Collection built. {len(collection.cards)} cards in collection")

            #Build directory structure and add cards

        except Exception as e:
            logging.error(f'Fatal error occurred: {e}')
    #TODO: select appropriate Exception and handle
    except:
        pass

main()