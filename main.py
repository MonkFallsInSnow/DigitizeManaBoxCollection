import logging
from Arguments.arguments import parse_arguments
from DataManagers.dataHandler import DataHandler

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("Logs/card_digitizer.log"),
            logging.StreamHandler()
        ]
    )


def main():
    try:
        setup_logging()
        logging.info("Starting MTG Card Digitizer")

        # Parse command line arguments
        args = parse_arguments()

        # Read and clean CSV data
        logging.info(f"Reading card data from {args.input_csv}...")
        data_handler = DataHandler(args.input_csv)
        raw_data = data_handler.get_data()
        logging.info(f"Found {len(raw_data)} unique cards in the CSV file.")

    except:
        pass

main()