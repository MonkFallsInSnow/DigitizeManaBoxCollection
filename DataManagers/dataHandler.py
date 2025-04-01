import logging
import pandas as pd
from Constants.headers import CSVHeaders

class DataHandler:
    def __init__(self, file_path):
        self._file_path = file_path
        self._df = None
        self._required_headers = {
            CSVHeaders.SCRYFALL_ID.value,
            CSVHeaders.QUANTITY.value,
            CSVHeaders.NAME.value,
            CSVHeaders.SET_NAME.value
        }

    @property
    def file_path(self):
        return self._file_path

    def _validate_data(self):
        columns = set()

        try:
            self._df = pd.read_csv(self._file_path)
            self._df.columns = self._df.columns.str.lower()
            columns = set(self._df.columns)

            if not self._required_headers.issubset(columns):
                raise ValueError
        except ValueError:
            missing_headers = ', '.join(self._required_headers - columns)
            logging.error(f'CSV file must contain the following header(s): {missing_headers}')
            raise
        except Exception as e:
            logging.error(f'Error reading CSV file: {e}')
            raise


    def _clean_data(self):
        # Remove rows with empty Scryfall IDs
        clean_df = self._df.dropna(subset=[CSVHeaders.SCRYFALL_ID.value, CSVHeaders.QUANTITY.value])

        # Convert Quantity to integer, replace invalid values with 1
        clean_df[CSVHeaders.QUANTITY.value] = (pd.to_numeric(clean_df[CSVHeaders.QUANTITY.value], errors='coerce').
                                                fillna(1).
                                                astype(int))

        # Group by Scryfall ID and sum quantities
        grouped_df = clean_df.groupby(CSVHeaders.SCRYFALL_ID.value, as_index=False).agg({
            CSVHeaders.QUANTITY.value: 'sum',
            CSVHeaders.NAME.value: 'first',
            CSVHeaders.SET_NAME.value: 'first'
        })

        # Convert to dictionary format
        card_data = {
            row[CSVHeaders.SCRYFALL_ID.value]: {
                CSVHeaders.QUANTITY.value: row[CSVHeaders.QUANTITY.value],
                CSVHeaders.NAME.value: row[CSVHeaders.NAME.value],
                CSVHeaders.SET_NAME.value: row[CSVHeaders.SET_NAME.value]
            }
            for _, row in grouped_df.iterrows()
        }

        logging.info(f'Found {len(card_data)} unique cards in the CSV file')
        return card_data

    def get_data(self):
        try:
            self._validate_data()
            return self._clean_data()
        except Exception as e:
            logging.error(f'Error parsing CSV file: {e}')
            raise




