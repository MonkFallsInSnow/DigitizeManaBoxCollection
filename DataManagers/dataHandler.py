import logging
import pandas as pd
from Constants.headers import CSVHeaders
from Utils.Exceptions.missingCSVHeaderError import MissingCSVHeaderError

class DataHandler:
    def __init__(self, file_path):
        self._file_path = file_path
        self._df = None
        self._required_headers = {
            CSVHeaders.SCRYFALL_ID,
            CSVHeaders.QUANTITY,
            CSVHeaders.NAME,
            CSVHeaders.SET_NAME
        }

    @property
    def file_path(self):
        return self._file_path

    def _validate_data(self):
        try:
            self._df = pd.read_csv(self._file_path)
            self._df.columns = self._df.columns.str.lower()
            columns = set(self._df.columns)

            if not self._required_headers.issubset(columns):
                missing_headers = ', '.join(self._required_headers - columns)
                raise MissingCSVHeaderError(self._file_path, self._required_headers, missing_headers)
        except MissingCSVHeaderError as e:
            logging.error(f'{self._file_path} is missing the following header(s): {e.missing_headers}')
            raise
        except Exception as e:
            logging.error(f'Error validating {self._file_path}: {e}')
            raise


    def _clean_data(self):
        # Remove rows with empty Scryfall IDs
        cleaned_df = self._df.dropna(subset=[CSVHeaders.SCRYFALL_ID.value, CSVHeaders.QUANTITY.value])

        # Convert Quantity to integer, replace invalid values with 1
        cleaned_df[CSVHeaders.QUANTITY] = (pd.to_numeric(cleaned_df[CSVHeaders.QUANTITY], errors='coerce').
                                                 fillna(1).
                                                 astype(int))

        # Group by Scryfall ID and sum quantities
        grouped_df = cleaned_df.groupby(CSVHeaders.SCRYFALL_ID, as_index=False).agg({
            CSVHeaders.QUANTITY.value: 'sum',
            CSVHeaders.NAME.value: 'first',
            CSVHeaders.SET_NAME.value: 'first'
        })

        # Convert to dictionary format
        cleaned_data = {
            row[CSVHeaders.SCRYFALL_ID]: {
                CSVHeaders.QUANTITY.value: row[CSVHeaders.QUANTITY],
                CSVHeaders.NAME.value: row[CSVHeaders.NAME],
                CSVHeaders.SET_NAME.value: row[CSVHeaders.SET_NAME]
            }
            for _, row in grouped_df.iterrows()
        }

        return cleaned_data

    def get_data(self):
        try:
            self._validate_data()
            return self._clean_data()
        except Exception:
            logging.error(f'Unable to parse {self._file_path}')
            raise


