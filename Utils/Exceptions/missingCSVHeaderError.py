class MissingCSVHeaderError(Exception):
    def __init__(self, csv_file, required_headers, missing_headers):
        super().__init__(f'Required header(s) missing from {csv_file}. '
                         f'Required: {required_headers}. Missing: {missing_headers}'
                         )

        self.missing_headers = missing_headers

