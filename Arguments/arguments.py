import argparse
import logging
import os
from pathlib import Path
from Constants.argumentOptions import OrganizationOptions

def _validate_input_csv(file_path):
    """
    Validate that the input CSV file exists.

    Args:
        file_path: Path to the input CSV file
    Returns:
        Valid file path
    Raises:
        argparse.ArgumentTypeError: If the file does not exist
    """
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f'Input file not found: {file_path}')

    return file_path


def _validate_output_dir(dir_path):
    """
    Validate that the output directory exists or create it if it doesn't.

    Args:
        dir_path: Path to the output directory
    Returns:
        Valid directory path
    Raises:
        argparse.ArgumentTypeError: If the path is not a directory
    """
    path = Path(dir_path)

    if not path.is_dir():
        raise argparse.ArgumentTypeError(f'Output path must be a directory: {dir_path}')

    if not path.exists():
        print(f'Creating output directory: {dir_path}')
        path.mkdir(parents=True)

    return dir_path

def _validate_organization_arg_group(args):
    org_options = []
    if args.color:
        org_options.append(OrganizationOptions.COLOR.value)
    if args.type:
        org_options.append(OrganizationOptions.TYPE.value)
    if args.set:
        org_options.append(OrganizationOptions.SET.value)
    if args.rarity:
        org_options.append(OrganizationOptions.RARITY.value)

    # If no options selected, use default
    if not org_options:
        args.color = True
        args.type = True
        org_options = [OrganizationOptions.COLOR.value, OrganizationOptions.TYPE.value]
        logging.info(f'Using default organization options: {' and '.join(org_options)}')

    return org_options

def parse_arguments():
    """
    Parse command line arguments for the MTG Card Digitizer application.

    Returns:
        Namespace containing parsed arguments
    """
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
        '--image_size', '-i',
        choices=['small', 'normal', 'large', 'border_crop'],
        default='normal',
        help='Image size returned by Scryfall API (Default: normal)'
    )

    # Organization options
    org_group = parser.add_argument_group('Organization options')
    org_group.add_argument(
        '--color', '-c',
        action='store_true',
        help='Organize by color'
    )
    org_group.add_argument(
        '--type', '-t',
        action='store_true',
        help='Organize by card type'
    )
    org_group.add_argument(
        '--set', '-s',
        action='store_true',
        help='Organize by set'
    )
    org_group.add_argument(
        '--rarity', '-r',
        action='store_true',
        help='Organize by rarity'
    )

    args = parser.parse_args()
    args.organization = _validate_organization_arg_group(args)

    return args
