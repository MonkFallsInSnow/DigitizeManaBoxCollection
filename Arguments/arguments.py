import argparse
import os
from pathlib import Path

def _validate_input_csv(file_path):
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f'Input file not found: {file_path}')

    return file_path


def _validate_output_dir(dir_path):
    path = Path(dir_path)

    if not path.is_dir():
        raise argparse.ArgumentTypeError(f'Output path must be a directory: {dir_path}')

    if not path.exists():
        print(f'Creating output directory: {dir_path}')
        path.mkdir(parents=True)

    return dir_path

def parse_arguments():
    parser = argparse.ArgumentParser(description='Digitize Magic: The Gathering card collection')

    parser.add_argument(
        'input_csv',
        type=_validate_input_csv,
        help='Path to a CSV file containing card data'
    )
    parser.add_argument(
        'output_dir',
        type=_validate_output_dir,
        help='Path to a directory that will store the output'
    )
    parser.add_argument(
        '--image-size', '-s',
        choices=['small', 'normal', 'large', 'border_crop'],
        default='normal',
        help='Image size returned by Scryfall API (Default: normal)'
    )

    return parser.parse_args()